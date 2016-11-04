import numpy as np
import math

class pthRootOfUnity():
    """ Class to hold p^th roots of unity symbolically over finite fields.
        These guys have the form
                                exp(2 pi i / p)
        where p is the characteristic of the field.

        They can be evaluated both symbolically and also exactly by 
        explicitly computing the value listed above using numpy. 
        Here we'll implement only what we need: exponents and multiplication.
    """

    def __init__(self, p, e = 1):
        """ Initialize a pth root of unity.
            Member variables:
            p - The characteristic of the underlying field. Should be prime.
                 Element takes the form of exp(2 pi i / p)
            e - The exponent, e.g. w^e. Default is 1.
        """
        # TODO some sort of primality check
        if p < 2:
            print ("Error, please enter a prime to make roots of unity.")
        else:
            self.p = p
            self.e = e


    def __mul__(self, op):
        """ Multiplication. These guys are cyclic: 
                      w^0 = 1, w^1 = w, w^2 = ..., w^p = 1,
            and so on. So we just need to add the exponents and get the
            result mod p.
        """
        if self.p != op.p:
            print("Error, cannot multiply roots of unity from different primes.")
            return 

        new_exp = (self.e + op.e) % self.p
        return pthRootOfUnity(self.p, new_exp)  


    def __imul__(self, op):
        """ Multiplication with assignment. """
        return self * op


    def __truediv__(self, op):
        """ Division. Same idea as multiplication. """
        if self.p != op.p:
            print("Error, cannot divide roots of unity from different primes.")
            return 

        new_exp = (self.e - op.e) % self.p
        return pthRootOfUnity(self.p, new_exp)  


    def __itruediv__(self, op):
        """ Division with assignment. """
        return self / op


    def __pow__(self, exponent):
        """ Exponentiation. Just multiply by exponent and take it
            modulo the prime. """
        new_exp = (self.e * exponent) % self.p
        return pthRootOfUnity(self.p, new_exp)  

            
    def __eq__(self, op):
        """ Test equality of two field elements """
        if self.p != op.p:
            return False
        if self.e != op.e:
            return False
        return True


    def __repr__(self):
        """ Make the field element get printed in the command line."""
        return ("w^" + str(self.e))


    def eval(self):
        """ Compute the actual number. Gross. """
        return pow(np.exp(2 * np.pi * 1j / self.p), self.e)


    def print(self):
        print("w^" + str(self.e))
