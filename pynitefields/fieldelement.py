"""
Class for an actual element of the field. Contains all the 
relevant operations. The GaloisField class should store an
array of these when it creates the field.

This is separate from the main field so that it has it's own type
and we can do things like
GF8[4] + GF8[2],
rather than
GF8.add(4, 2)
and thus store the field elements in individual variables for
later use.
"""

import math

class FieldElement():
    """
    Initialize a field element given the field dimensions
    and the expansion coefficients.
    """
    def __init__(self, p, n, exp_coefs):
        self.p = p
        self.n = n
        self.dim = int(math.pow(p, n))

        # Set the expansion coefficients.
        # If we're in a prime field, the basis is 1, and
        # the coefficient is just the value
        self.exp_coefs = exp_coefs

        self.field_list = []


    """
    Add two elements together. Simple modulo for primes, 
    need to deal with the coefficients modulo p for the 
    extended case.
    """
    def __add__(self, el):
        # Make sure we're in the same field!
        if self.p != el.p:
            print("Error, cannot add elements from different fields!")
            return None
        if self.n != el.n:
            print("Error, cannot add elements from different fields!")
            return None

        # Prime case
        if self.n == 1:
            return FieldElement(self.p, self.n, [(self.exp_coefs[0] + el.exp_coefs[0]) % self.p])
        # Power of prime case
        else:
            # Coefficients simply add modulo p
            new_coefs = [(self.exp_coefs[i] + el.exp_coefs[i]) % self.p for i in range(0, self.n)]
            return FieldElement(self.p, self.n, new_coefs)
    
    """
    Compute the difference of two elements. Simple modulo for primes, 
    need to deal with the coefficients modulo p for the 
    extended case.
    """
    def __sub__(self, el):
        # Make sure we're in the same field!
        if self.p != el.p:
            print("Error, cannot subtract elements from different fields!")
            return None
        if self.n != el.n:
            print("Error, cannot subtract elements from different fields!")
            return None

        # Prime case
        if self.n == 1:
            return FieldElement(self.p, self.n, [(self.exp_coefs[0] - el.exp_coefs[0]) % self.p])
        # Power of prime case
        else:
            # Coefficients subtract modulo p
            new_coefs = [(self.exp_coefs[i] - el.exp_coefs[i]) % self.p for i in range(0, self.n)]
            return FieldElement(self.p, self.n, new_coefs)


    """
    Compute the product of two elements. Simple modulo for primes, 
    need to deal with the coefficients modulo p for the 
    extended case.
    """
    def __mul__(self, el):
        # Multiplication by a constant
        if isinstance(el, int):
            return FieldElement(self.p, self.n, [(el * exp_coef) % self.p for exp_coef in self.exp_coefs] )
        elif isinstance(el, FieldElement):
            # Make sure we're in the same field!
            if self.p != el.p:
                print("Error, cannot multiply elements from different fields!")
                return None
            if self.n != el.n:
                print("Error, cannot multiply elements from different fields!")
                return None


            # Prime case
            if self.n == 1:
                return FieldElement(self.p, self.n, [(self.exp_coefs[0] * el.exp_coefs[0]) % self.p])
            # Power of prime case
            else:
                # I stored the whole list of field elements in each element for a reason...
                # Now we can multiply really easily
                power_self = self.field_list.index(self)
                power_el = self.field_list.index(el)

                if power_el == 0 or power_self == 0:
                    return self.field_list[0]
                else:
                    new_exp = power_self + power_el
                    # Overflow
                    if new_exp > self.dim - 1:
                        new_exp = ((new_exp - 1) % (self.dim - 1)) + 1
                    return self.field_list[new_exp]
        else:
            raise TypeError("Unsupported operator")

 
    """
    Division - multiply by the inverse. Always make sure we're not
    dividing by zero!
    """
    def __truediv__(self, el):
        if isinstance(el, FieldElement):
            if self.n != el.n:
                print("Error, cannot divide elements from different fields.")
            if self.p != el.p:
                print("Error, cannot divide elements from different fields.")

            # Prime
            if self.n == 1:
                if self.exp_coefs[0] == 0:
                    print("Error! Cannot divide by 0, silly.")
                    return

            # Power of prime
            else:
                if self.field_list.index(self) == 0:
                    print("Error! Cannot divide by 0, silly.")
                    return

            # Actually do the division 
            return self * el.inv()


    """
    Compute the power. Simple modulo for primes, 
    need to wrap around the exponents for power of primes.
    """
    def __pow__(self, exponent):
        # Prime case
        if self.n == 1:
            return FieldElement(self.p, self.n, [int(math.pow(self.exp_coefs[0], exponent)) % self.p])
        # Power of prime case
        else:
            new_exp = self.field_list.index(self) * exponent
            if new_exp > self.dim - 1:
                new_exp = ((new_exp - 1) % (self.dim - 1)) + 1
            return self.field_list[new_exp]
            

    """
    Make the field element appear in the command line.
    """
    def __repr__(self):
        if self.n == 1:
            return str(self.exp_coefs[0])
        else:
            return str(self.exp_coefs)


    """
    Compute the multiplicative inverse of the field elements.
    All elements have a multiplicative inverse except 0.
    """
    def inv(self):
        # Prime case - brute force :(
        if self.n == 1:
            if self.exp_coefs[0] == 0:
                print("Error, 0 has no multiplicative inverse.")
                return

            for i in range(0, self.p):
                if (self.exp_coefs[0] * i) % self.p == 1:
                    return FieldElement(self.p, self.n, [i])
        else:
            my_index = self.field_list.index(self)
            if my_index == 0:
                print("Error, 0 has no multiplicative inverse.")
                return 
            # Last element is always 1 which is it's own inverse
            elif my_index == self.dim - 1:
                return self.field_list[self.dim - 1]
            # All other elements, find exponent which sums to dim - 1
            else:
                return self.field_list[self.dim - my_index - 1]


    """ 
    Compute the trace. The formula just relies on the pow function so
    it has the same implementation for prime and powers of prime.
    The sum should be an element of the base field for power of prime case.
    """
    def tr(self):
        sum = self

        for i in range(1, self.n):
            sum = sum + pow(self, pow(self.p, i))

        if self.n == 1:
            return sum
        else:
            return sum.exp_coefs[0]


    """ 
    Print out information about the element.
    """
    def print(self):
        if self.n == 1:
            print(self.exp_coefs[0])
        else:
            print(self.exp_coefs)
