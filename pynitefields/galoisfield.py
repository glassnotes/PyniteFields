#!/usr/bin/python3

import sys
import math

from pynitefields.fieldelement import FieldElement

class GaloisField():
    """
    Initialize the Galois Field based on user input.

    Default parameters for a prime field, additional parameters are
    for the case of a field extension.

    p should be a prime number, n some exponent greater than 1 (if used).
    coefs are the coefficients of an irreducible polynomial in list format
    (if used). 

    EXAMPLE:
    GF3 = GaloisField(3) # Produces the Galois field of order 3
    GF8 = GaloisField(2, 3, [1, 0, 1, 1]) # GF of order 8, 
                                          # with polynomial 1 + x^2 + x^3

    GaloisField has a number of member variables:
    p - The prime dimension of the field
    n - The degree of the field extension (1 if just a prime field) 
    dim - The dimension of the space, p^n
    coefs - The coefficients of the irreducible polynomial
    elements - A list of all elements in the finite field, of class FieldElement
    bool_sdb - A boolean which tells us whether the expansions are in the self-dual
               basis (True) or the polynomial basis (False). The default is False.
    """
    def __init__(self, p, n = 1, coefs = []):
        # TODO implement check for prime number
        self.p = p

        # Field extension parameter. 
        # Base prime field if n = 1, otherwise the field is GF(p^n)
        if n > 1:
            self.n = n
        elif n != 1:
            print("Error, invalid exponent for field extension.")
            print("Please enter an exponent n of 2 or greater.\n")
            sys.exit()
        else:
            self.n = 1
            self.coefs = []
        
        # Set separate parameter for the field dimension
        self.dim = int(math.pow(p, n))

        # Initialize the coefficients for the irreducible polynomial 
        # to do the field extension with. 
        if len(coefs) > 0:
            # We should have n + 1 coefficients for GF(p^n)
            if len(coefs) == n + 1:
                self.coefs = coefs
            else:
                print("Error, invalid number of coefficients in the irreducible polynomial.")
                print("Field of size " + str(self.p) + "^" + str(self.n) + " should have ", end = "")
                print(str(n + 1) + " coefficients in its irreducible polynomial.")
                sys.exit()


        # Generate the actual field elements
        if self.n == 1:
            # Prime case is easy. No field basis, just the numbers from 0 to p,
            # stored as FieldElements.
            self.elements = []
            for i in range(0, p):
                self.elements.append(FieldElement(self.p, self.n, [i]))
        else:
            # Use the irreducible polynomial to generate the field elements
            # They'll be stored in order as a list of coefficients in the polynomial basis
            # e.g. in dim 4, x^2 + x + 1 is the polynomial, use the basis (1, x) and store
            # the elements as:
            # 0 -> [0, 0], 1 -> [1, 0], x -> [1, 0], x^2 = [1, 1]

            # Hold all the coefficients for each element
            # For simplicity, rather than a list of list, represent each field element as a 
            # string of coefficients, i.e. [0, 1, 1] -> "011"  
            field_list = []

            # The polynomial basis contains n elements
            # The first element is always 0
            self.elements = []
            self.elements.append(FieldElement(self.p, self.n, [0]*self.n))
            field_list.append("0" * self.n)

            # The next few elements are initial terms in the poly basis (i.e. x, x^2 ...)
            for i in range(1, self.n):
                next_coefs = [0]*(i) + [1] + [0]*(self.n - i - 1) 
                self.elements.append(FieldElement(self.p, self.n, next_coefs))
                field_list.append("".join([str(x) for x in next_coefs]))

            # For the n^th power of x, we need to use the irreducible polynomial
            nth_coefs = [((-1) * self.coefs[i]) % self.p for i in range(0, self.n)]
            self.elements.append(FieldElement(self.p, self.n, nth_coefs))
            field_list.append("".join([str(x) for x in nth_coefs]))

            # For the remaining powers, multiply the previous element by primitive element
            for el in range(self.n + 1, self.dim):
                # Shift all coefficients ahead by 1 power of x and take the sum because
                # we know all the previous elements, and will never get anything 
                # with such a high exponent we don't know it's basis coefficients
                next_coefs = [0] + self.elements[el - 1].exp_coefs
                
                # Get a list of the powers whose coefficients aren't 0
                which_to_sum = [self.elements[i] * coeff for i, coeff in enumerate(next_coefs) if coeff != 0]
                sum = self.elements[0]

                for sum_el in which_to_sum:
                    sum = sum + sum_el

                # TODO Make sure that this element is not already in the list - if it is, then
                # we did not use a true primitive polynomial.
                str_rep = "".join([str(x) for x in sum.exp_coefs])
                if str_rep not in field_list:
                    self.elements.append(sum)
                    field_list.append(str_rep)
                else:
                    raise ValueError("Repeated field element detected; please make sure your irreducible polynomial is primitive.")
                 
            # This is really dumb, but make sure each element holds a copy of the whole
            # list of the field elements. This makes field multiplication way easier.
            for i in range(len(self.elements)):
                (self.elements[i]).field_list = field_list 
                (self.elements[i]).prim_power = i

        # By default, we are using the polynomial basis
        self.bool_sdb = False


    def __getitem__(self, index):
        """ Return element i (prime) or x^i (power of prime) of the field."""
        if index < self.dim:
            return self.elements[index]
        else:
            print("Error, element out of bounds.")


    def __iter__(self):
        """ Make the finite field iterable; return an iterator to the field elements."""
        return iter(self.elements)


    def to_sdb(self, sdb_element_indices):
        """ Transform the expansions coefficients to the self-dual basis.

        Valid only for power of prime fields. For now, assume that the 
        user will provide the powers of the primitive element which can 
        be used as a self-dual basis (later, we will implement this ourselves.
        """

        if self.n == 1:
            print("Cannot take self-dual basis of a prime field.")
            return

        if self.verify_sdb(sdb_element_indices) == False:
            print("Invalid self-dual basis provided.")
            return


        # If all goes well, we can start computing the coefficients
        # in terms of the new elements by using the trace and multiplication
        # functions.
        new_elements = []
        field_list = []

        sdb = [self.elements[sdb_element_indices[i]] for i in range(0, self.n)]

        for element in self.elements:
            sdb_coefs = [] # Expansion coefficients in the sdb

            for basis_el in sdb:
                sdb_coefs.append(tr(element * basis_el))

            new_elements.append(FieldElement(self.p, self.n, sdb_coefs))
            field_list.append("".join([str(x) for x in sdb_coefs]))

        self.elements = new_elements
        for i in range(len(self.elements)):
            (self.elements[i]).field_list = field_list 
            (self.elements[i]).prim_power = i
    

        self.bool_sdb = True


    def is_sdb(self):
        """ Query the field to determine if we're in sdb or polynomial basis."""
        return self.bool_sdb


    def verify_sdb(self, sdb_element_indices):
        """ Verify if a set of elements form a self-dual basis.

        Check two things here:
        - The trace of each basis element with itself is 1.
        - The trace of each basis element with every other is 0 (orthogonality). 

        Return True if it's a self-dual basis, False if not.
        """
        if len(sdb_element_indices) != self.n:
            print("Error, incorrect number of elements in proposed basis.")
            return False

        for i in range(0, self.n):
            for j in range(i, self.n): # Don't double compute things
                trace_result = tr(self.elements[sdb_element_indices[i]] * self.elements[sdb_element_indices[j]])

                if i == j: # Same element, should have trace 1
                    if trace_result != 1:
                        return False
                else: # Different elements should be orthogonal and have trace 0
                    if trace_result != 0:
                        return False

        return True


    def compute_sdb(self):
        """ Compute a self-dual basis for this field."""

        # Compute a short list who's trace of their square is equal to 1
        first_round = []   
        for element in self.elements:
            if tr(element * element) == 1:
                first_round.append(element)
    
        for element in first_round:
            print(element)

        second_round = []

        # Of the remaining possible elements, compute traces and see 
        # if we can find n of them which equal 0
        for i in range(0, len(first_round)):
            traces = [tr(first_round[i] * first_round[j]) for j in range(0, len(first_round))] 
            if traces.count(0) == self.n:
                second_round.append(first_round[i])
                print(traces)

        print(second_round)

        return

    def to_poly(self):
        """ Transform the expansions coefficients to the polynomial basis.

        Broken!! Do not use this yet.
        Only needs to be done if we are currently in the self-dual basis.
        """

        print("Do not use me yet!")
        return

        """
        if self.n == 1:
            print("Cannot take self-dual basis of a prime field.")
            return

        if self.bool_sdb == False:
            print("Already in the polynomial basis!")
            return

        # If all goes well, we can start computing the coefficients
        # in terms of the new elements by using the trace and multiplication
        # functions.
        new_elements = []

        poly_basis = [self.elements[-1]] + self.elements[1:self.n]

        for element in self.elements:
            poly_coefs = [] # Expansion coefficients in the sdb

            for basis_el in poly_basis:
                poly_coefs.append(tr(element * basis_el))

            new_elements.append(FieldElement(self.p, self.n, poly_coefs))

        for element in new_elements:
            element.field_list = new_elements
    
        self.elements = new_elements
        """

    def evaluate(self, coefs, argument):
        """ Evaluate the effect of a curve on a finite field element.
            The information about the curve is stored in the poly_coefs
            argument. For example, if we wish to evaluate the curve
            beta(alpha) = f[3] + 2 alpha + f[5] alpha^2 on the field
            element f[1], then we would call this function as

            f.evaluate([f[3], 2, f[5]], f[1])
        """
        result = coefs[0] * self.elements[-1] 
        print(result)
        for coef_idx in range(1, len(coefs)):
            result += coefs[coef_idx] * pow(argument, coef_idx)
            print(result)
        return result

    def print(self):
        """ Print out a wealth of useful information about the field."""
        
        print("--- Galois field information ---")
        print("p = " + str(self.p))

        if self.n > 1:
            print("n = " + str(self.n))

            print("\nIrreducible polynomial: ", end = "")
            if self.coefs[0] == 1:
                print("1 + ", end ="")

            for i in range(1, len(self.coefs)):
                if self.coefs[i] != 0:
                    # Print coefficient if it's not 1
                    if self.coefs[i] != 1:
                        print(str(self.coefs[i]), end = "") 

                    # Print exponent value
                    print("x", end = "")
                    if i != 1:
                        print("^" + str(i), end = "")

                    if i != len(self.coefs) - 1: 
                        print(" + ", end = "")

        print("\nField elements:")
        for element in self.elements:
            element.print()


def tr(x):
    """ Wrapper trace function so the user can do tr(x) or x.trace()."""
    # Make sure x is a field element
    if type(x) is not FieldElement:
        print("Error, invalid argument to function 'tr'.")
        return None
    else:
        return x.tr()


def inv(x):
    """ Wrapper so the user can do x.inv() or inv(x) interchangeably."""
    # Make sure x is a field element
    if type(x) is not FieldElement:
        print("Error, invalid argument to function 'inv'.")
        return None
    else:
        return x.inv()


