#!/usr/bin/python                                                                  
# -*- coding: utf-8 -*-                                                            
#                                                                                  
# galoisfield.py: Implementation of a full finite field. 
#                                                                                  
# © 2016 Olivia Di Matteo (odimatte@uwaterloo.ca)                                  
#                                                                                  
# This file is part of the project PyniteFields.                                      
# Licensed under BSD-3-Clause                                                      
# 

import sys
import math

from pynitefields.fieldelement import FieldElement
from pynitefields.pthrootofunity import pthRootOfUnity

class GaloisField():
    """ A finite field, or Galois field.

        Args:
            p (int): A prime number, the base of the field.
            n (int): An exponent representing the degree of a field extension.
                     By default n = 1 (prime field).
            coefs (list): A list of integers representing the coefficients of
                          an irreducible primitive polynomial of degree n over
                          GF(p). Default is the empty list for prime fields.

        Attributes:
            p (int): The prime dimension of the field
            n (int): The degree of the field extension 
            dim (int): The full order of the field, :math:`p^n`.
            w (pthRootOfUnity): The :math:`p^{\\text{th}}` root of unity.

            coefs (list): The coefficients of the irreducible polynomial
            elements (list): A list of all FieldElements in this finite field.
            bool_sdb (bool): A boolean which tells us whether the elements'
                             expansion coefficients are in the self-dual
                             basis (True) or the polynomial basis (False). 
                             The default is False.
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

        # Initialize the pth root of unity
        self.w = pthRootOfUnity(p)

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


    def __getitem__(self, idx):
        """ Access specific elements in the finite field.

            Args:
                idx (int): The index of the element to retrieve. For primes 
                    this is the same as the number itself; for power-of-primes
                    it represents the power of the primitive element.
          
            Returns:
                The element at the specified index in the field. 

              None if idx is out of bounds.
        """
        if idx < self.dim and idx >= 0:
            return self.elements[idx]
        else:
            print("Error, element out of bounds.")


    def __iter__(self):
        """ Make the finite field iterable. 

            Returns:
                An iterator to the field elements.
        """
        return iter(self.elements)


    def to_sdb(self, sdb_element_indices):
        """ Transform the expansions coefficients to the self-dual basis.

            Currently valid only for fields whose orders are powers of 2.

            Args:
                sdb_element_indices (list): The indices of the FieldElements 
                    (as powers of the primitive element) that represent the
                    self-dual basis. e.g. if the self-dual basis is 
                    :math:`\{ \sigma^3, \sigma^5, \sigma^6 \}`, this list
                    would be [3, 5, 6].

            TODO:
                Implement automatic construction of some self-dual basis.
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
        """ Checks if a field is expressed in the self-dual basis.
        
            Returns:
                True if the elements are expressed in the self-dual basis, 
                false if otherwise.

            TODO Remove this function and just rename bool_sdb to is_sdb.
        """
        return self.bool_sdb


    def verify_sdb(self, sdb_element_indices):
        """ Verify if a set of elements form a proper self-dual normal basis.

            Check two things here:
              * The trace of each basis element multiplied by itself is 1.
              * The trace of each basis element multiplied by every other is 
                0 (orthogonality). 

            Returns:
                True if above conditions are satisfied, false if not. 
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
        """ Compute a self-dual basis for this field.
       
            .. warning::
                DO NOT USE, still under development.
        """

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
            I'm lazy, so just return a fresh field.

            .. warning::

                I don't think this works.
        """
        self = GaloisField(self.p, self.n, self.coefs)


    def evaluate(self, coefs, argument):
        """ Evaluate a function, or curve on a finite field element.

            We consider here functions of the form
            
            .. math::
              
              f(\\alpha) = c_0 + c_1 \\alpha + \cdots + c_n \\alpha^n

            This function is primarily meant for use with the Curve class in
            my Balthasar package.

            Args:
                coefs (list): A set of coefficients for the curve, i.e.
                              :math:`[c_0, c_1, \ldots, c_n]`. These should
                              be a mix of integers and FieldElements.
                argument (FieldElement): The argument to the function, i.e.
                      the :math:`\\alpha` in :math:`f(\\alpha)`.
              
            Returns:
                The value of the function of the argument, taken over the
                finite field.
        """
        result = coefs[0] * self.elements[-1] 
        for coef_idx in range(1, len(coefs)):
            result += coefs[coef_idx] * pow(argument, coef_idx)
        return result


    def print(self):
        """ Print out all the useful information about a field."""
        
        print("--- Galois field information ---")
        print("p = " + str(self.p))

        if self.n > 1:
            print("n = " + str(self.n))

            print("\nIrreducible polynomial: ", end = "")
            if self.coefs[0] != 0:
                print(str(self.coefs[0]) + " + ", end ="")

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


def gchar(x):
    """ Wrapper so the user can do x.gchar() or gchar(x). """
    if type(x) is not FieldElement:
        print("Error, invalid argument to function 'gchar'.")
        return None
    else:
        return x.gchar()


def inv(x):
    """ Wrapper so the user can do x.inv() or inv(x) interchangeably."""
    # Make sure x is a field element
    if type(x) is not FieldElement:
        print("Error, invalid argument to function 'inv'.")
        return None
    else:
        return x.inv()


