#!/usr/bin/python3

import sys
import math

from fieldelement import *

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
        # TODO check for valid polynomials
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
            # They will be stored in order as a list of coefficients in the polynomial basis
            # e.g. in dimension 4, x^2 + x + 1 is the polynomial, use the basis (1, x) and store
            # the elements as:
            # 0 -> [0, 0], 1 -> [1, 0], x -> [1, 0], x^2 = [1, 1]

            # The polynomial basis contains n elements
            # The first element is always 0
            self.elements = []
            self.elements.append(FieldElement(self.p, self.n, [0]*self.n, self.coefs))

            # The next few elements are the initial terms in the polynomial basis (i.e. x, x^2 ...)
            for i in range(1, self.n):
                next_coefs = [0]*(i) + [1] + [0]*(self.n - i - 1) 
                self.elements.append(FieldElement(self.p, self.n, next_coefs, self.coefs))

            # For the n^th power of x, we need to use the irreducible polynomial
            nth_coefs = [((-1) * self.coefs[i]) % self.p for i in range(0, self.n)]
            self.elements.append(FieldElement(self.p, self.n, nth_coefs, self.coefs))

            # For the remaining powers, use multiplication of previous element with primitive element
            for el in range(self.n + 1, self.dim):
                # Shift all coefficients ahead by 1 power of x and then take the sum because
                # we know all the previous elements, and will never get anything so big we don't know it
                next_coefs = [0] + self.elements[el - 1].exp_coefs
                
                # Get a list of the powers whose coefficients aren't 0
                which_to_sum = [self.elements[i] * coeff for i, coeff in enumerate(next_coefs) if coeff != 0]
                sum = self.elements[0]

                for sum_el in which_to_sum:
                    sum = sum + sum_el

                self.elements.append(sum)
                 
            # This is really dumb, but make sure each element holds a copy of the whole
            # list of the field elements. This makes field multiplication infinitely easier.
            for element in self.elements:
                element.field_list = self.elements


    """ 
    Return the coefficient list for element x^i of the field.
    """
    def __getitem__(self, index):
        if index < self.dim:
            return self.elements[index]
        else:
            print("Error, element out of bounds.")


    """
    Print out a wealth of useful information about the field.
    """
    def print(self):
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


def main():
    GF3 = GaloisField(3)
    GF3.print()

    """
    print("\n\n\n")
    GF8 = GaloisField(2, 5, [1, 1, 0, 1, 1, 0, 1])
    GF8.print()
    """


if __name__ == '__main__':
    main()
