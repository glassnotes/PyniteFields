import math

class FieldElement():
    """ Class for an element in a finite field.
    
    The class GaloisField stores an array of FieldElements().
    All field arithmetic operations are are implemented within the 
    FieldElement class.
     
    This is separate from the main field so that it has it's own type 
    and we can do things like 
    GF8[4] + GF8[2], 
    rather than 
    GF8.add(4, 2) 
    and thus store the field elements in individual variables for 
    later use. 

    Details about member variables:
    p - The prime dimension of the field this element is in
    n - The degree of the field extension (1 if prime field)
    dim - The full dimension of the field p^n
    exp_coefs - A list of expansion coefficients in the basis of choice
                (determined by the parent GaloisField class)
    str_rep   - A representation of this elements basis coefficients as a string
                (just the string version of exp_coefs)
    field_list - A copy of the list of all elements in the parent GaloisField.
                 Inclusion of this parameter is not ideal, but greatly
                 simplifies the implementation of many of the arithmetic 
                 operations (notably multiplication, inverse, exponentiation),
                 and specifically for power of prime fields.
                 With field_list, each element knows it's position, or power
                 of the primitive element in the field, which makes operations
                 which boil down to simple addition and multiplication of 
                 exponents of the primitive element on paper much simpler.
    """

    def __init__(self, p, n, exp_coefs, field_list = []):
        """ Create an element of the finite field.

        Initialize a field element given the field dimensions
        and the expansion coefficients.
        """
        self.p = p
        self.n = n
        self.dim = int(math.pow(p, n))

        # Set the expansion coefficients.
        # If we're in a prime field, the basis is 1, and
        # the coefficient is just the value
        self.exp_coefs = exp_coefs
        self.str_rep = "".join([str(x) for x in exp_coefs])
        self.prim_power = -1
        self.field_list = []

        # Prim power doesn't really make sense for prime, but set it here
        # so that we can make the rest of the code more general
        if self.n == 1:
            self.prim_power = exp_coefs[0]

        # This gets set by the GaloisField constructor after
        # ALL the field elements have been created. This is set only
        # for power of prime fields.
        if len(field_list) != 0:
            self.field_list = field_list 
            self.prim_power = self.field_list.index(self.str_rep)


    def __add__(self, el):
        """ Addition.

        Add two field elements together. Simple modulo for primes, 
        need to deal with the coefficients modulo p for the 
        extended case.
        """
        # Make sure we're in the same field!
        if (self.p != el.p) or (self.n != el.n):
            print("Error, cannot add elements from different fields!")
            return None

        # Prime case
        if self.n == 1:
            return FieldElement(self.p, self.n, [(self.prim_power + el.prim_power) % self.p])
        else: # Power of prime case
            # Coefficients simply add modulo p
            new_coefs = [(self.exp_coefs[i] + el.exp_coefs[i]) % self.p for i in range(0, self.n)]
            return FieldElement(self.p, self.n, new_coefs, self.field_list)


    

    def __sub__(self, el):
        """ Subtraction.

        Compute the difference of two elements. Simple modulo for primes, 
        need to deal with the coefficients modulo p for the 
        extended case.
        """
        # Make sure we're in the same field!
        if (self.p != el.p) or (self.n != el.n):
            print("Error, cannot subtract elements from different fields!")
            return None

        # Prime case
        if self.n == 1:
            return FieldElement(self.p, self.n, [(self.prim_power - el.prim_power) % self.p])
        else:  # Power of prime case
            # Coefficients subtract modulo p
            new_coefs = [(self.exp_coefs[i] - el.exp_coefs[i]) % self.p for i in range(0, self.n)]
            return FieldElement(self.p, self.n, new_coefs, self.field_list)


    def __mul__(self, el):
        """ Multiplication.

        Compute the product of two elements. Simple modulo for primes, 
        for power of primes we can use field_list to find out which power
        of the primitive element each operand is, and then add those together.
        """
        # Multiplication by a constant (must be on the right!)
        if isinstance(el, int):
            return FieldElement(self.p, self.n, [(el * exp_coef) % self.p for exp_coef in self.exp_coefs] , self.field_list)

        # Multiplication by another FieldElement
        elif isinstance(el, FieldElement):
            # Make sure we're in the same field!
            if (self.p != el.p) or (self.n != el.n):
                print("Error, cannot multiply elements from different fields!")
                return None

            # Prime case
            if self.n == 1:
                return FieldElement(self.p, self.n, [(self.prim_power * el.prim_power) % self.p])
            # Power of prime case
            else:
                # I stored the whole list of field elements in each element for a reason...
                # Now we can multiply really easily

                if el.prim_power == 0 or self.prim_power == 0: # Multiplying by 0, nothing to see here
                    new_exp_coefs = [int(x) for x in self.field_list[0]] 
                    return FieldElement(self.p, self.n, new_exp_coefs, self.field_list)
                else:
                    new_exp = self.prim_power + el.prim_power # New exponent
                    # If the exponent calculated is outside the range of primitive element
                    # powers of the field, we need to wrap it around using the fact that
                    # the last field element is 1.
                    if new_exp > self.dim - 1: 
                        new_exp = ((new_exp - 1) % (self.dim - 1)) + 1
                    new_exp_coefs = [int(x) for x in self.field_list[new_exp]] 
                    return FieldElement(self.p, self.n, new_exp_coefs, self.field_list)
        else:
            raise TypeError("Unsupported operator")

    def __rmul__(self, el): # Implementing rmul so we can multiply on the left by integers
        return self * el
        #if isinstance(el, int):
        #    return FieldElement(self.p, self.n, [(el * exp_coef) % self.p for exp_coef in self.exp_coefs] , self    .field_list)
 
    def __truediv__(self, el):
        """ Division.

        In a Galois Field division is just multiplying by the inverse. 
        Always make sure we're not dividing by 0, since 0 has no multiplicative inverse.
        """
        if isinstance(el, FieldElement):
            if (self.p != el.p) or (self.n != el.n):
                print("Error, cannot divide elements from different fields.")

            # Prime
            if self.n == 1:
                if self.prim_power == 0:
                    print("Error! Cannot divide by 0, silly.")
                    return
            # Power of prime
            else:
                if self.field_list.index(self.str_rep) == 0:
                    print("Error! Cannot divide by 0, silly.")
                    return
            # Actually do the division 
            return self * el.inv()


    # Operations with assignment
    def __iadd__(self, el):
        """ Addition with assignment. """
        return self + el


    def __isub__(self, el):
        """ Subtraction with assignment. """
        return self - el


    def __imul__(self, el):
        """ Multiplication with assignment. """
        return self * el


    def __itruediv__(self, el):
        """ Division with assignment. """
        return self / el


    def __pow__(self, exponent):
        """ Exponentiation.

        Compute the power self^exponent. Simple modulo for primes, 
        need to wrap around the exponents for power of primes. For power of primes,
        we conventionally consider the primitive element to the 0'th power to be 0.
        """
        # Prime case
        if self.n == 1:
            return FieldElement(self.p, self.n, [int(math.pow(self.prim_power, exponent)) % self.p])
        # Power of prime case
        else:
            new_exp_coefs = []
            if self.prim_power == 0 or exponent == 0: # 0, and any element to the 0 is 0 by convention 
                new_exp_coefs = [int(x) for x in self.field_list[0]]
            else:
                new_exp = self.prim_power * exponent
                if new_exp > self.dim - 1:
                    new_exp = ((new_exp - 1) % (self.dim - 1)) + 1
                new_exp_coefs = [int(x) for x in self.field_list[new_exp]] 
            return FieldElement(self.p, self.n, new_exp_coefs, self.field_list)
            
    def __eq__(self, el):
        # Test equality of two field elements
        if (self.p != el.p) or (self.n != el.n):
            return False
        if self.exp_coefs != el.exp_coefs:
            return False
        if self.field_list != el.field_list:
            return False
        return True



    def __repr__(self):
        """ Make the field element get printed in the command line."""
        if self.n == 1:
            return str(self.prim_power)
        else:
            return str(self.exp_coefs)


    def inv(self):
        """ Inversion.

        Compute the multiplicative inverse of a field element.
        All elements have a multiplicative inverse except 0.
        """
        if self.n == 1: # Prime case - brute force :(
            if self.prim_power == 0:
                print("Error, 0 has no multiplicative inverse.")
                return

            for i in range(0, self.p):
                if (self.prim_power * i) % self.p == 1:
                    return FieldElement(self.p, self.n, [i])
        else: # Power of prime case
            if self.prim_power == 0:
                print("Error, 0 has no multiplicative inverse.")
                return 
            # Last element is always 1 which is it's own inverse
            elif self.prim_power == self.dim - 1:
                return self 
            # All other elements, find exponent which sums to dim - 1
            else:
                new_exp_coefs = [int(x) for x in self.field_list[self.dim - self.prim_power - 1]]
                return FieldElement(self.p, self.n, new_exp_coefs, self.field_list)


    def tr(self):
        """ Trace.

        Compute the trace of a field element. The formula just relies on the pow function so
        it has the same implementation for prime and powers of prime. The trace of any element 
        should be an element of the base field for the power of prime case.
        """
        sum = self

        if self.n > 1:
            for i in range(1, self.n):
                sum = sum + pow(self, pow(self.p, i))
        return sum.exp_coefs[0]


    def print(self):
        """ Print out information about the element."""
        if self.n == 1:
            print(self.prim_power)
        else:
            print(self.exp_coefs)
