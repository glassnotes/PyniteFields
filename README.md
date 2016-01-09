# PyniteFields
A class library for operations on finite fields (a.k.a. Galois fields) which I find useful in my line of work. PyniteFields is implemented in Python 3.

PyniteFields is meant to be fairly intuitive and easy to use. It's inspired by some of the ideas in the Mathematica
FiniteFields package, which is pretty great (except then you have to write everything _else_ in Mathematica too).

You can install PyniteFields as follows:
```
cd PyniteFields
python3 setup.py install
```

All operations are done with a single object of the class GaloisField. 

You can create a field with prime order like so (using order 5):
```
from pynitefields import * 
gf = GaloisField(5)
```

To create a field with power of prime order you'll need 3 things:
- A base prime _p_,
- An exponent _n_ such that the field has order _p<sup>n</sup>_,
- Coefficients for a primitive, irreducible polynomial with degree _n_.

For example, suppose we want to create the field GF(8). We know the irreducible polynomial
_1 + x + x<sup>3</sup>_, so we put it's coefficients into a list: [1, 1, 0, 1]. The _i_<sup>th</sup>
entry in the list corresponds to the coefficient attached to the _i_<sup>th</sup> power of the primitive element _x_.

To create the prime power field (using 8 as our example) we feed it the prime, exponent and coefficients in order:
```
gf = GaloisField(2, 3, [1, 1, 0, 1])
```


All subsequent operations can be achieved using the object ```gf``` which we have created.

We can grab the _i_<sup>th</sup> power of the primitive element using the [] operator:
```
gf[0]   # Returns the first element (i.e. 0)
gf[2]   # Returns the element x^2
gf[p^n - 1]  # Returns the last element of the field
```

Field elements are stored as lists of coefficients in the polynomial basis. For primes this
is very simple - the polynomial basis is just 1, so we store the elements themselves in a 
single item list. For power of primes, let's go back
to our example of dimension 8. Element _x<sup>3</sup>_ can be expressed as 1 + _x_, so 
it is stored as the list [1, 1, 0].

We can perform all four arithmetic operations on field elements, and take their powers and inverses:
```
gf[3] + gf[5]
gf[2] - gf[7]
gf[4] * gf[1]
gf[1] / gf[6]
pow(gf[4], 3)
inv(gf[2])
```

We can also take the trace, which is quite a useful operation:
```
gf[2].tr()
tr(gf[2])  # Same as above, but more convenient to write
``` 

=============================================================
Some more complicated functionality...

It is possible to convert the field such that all the elements are expanded in terms of a
self-dual basis rather than the polynomial basis. For example, suppose we are working in GF(4).
The elements _x_ and _x_<sup>2</sup> comprise a self-dual basis. To convert the field we can do
```
gf = GaloisField(2, 2, [1, 1, 1])
gf.to_sdb([1, 2])
```
Currenty, the program does not compute a self-dual basis for you - you will have to provide one yourself.
Here, to_sdb() takes as an argument a list of powers of the primitive element which
make up the self-dual basis. For more examples, see the table below.  


PyniteFields can evaluate functions, or curves, over field elements. Suppose you have some function  
 
_b_(_a_) = _x_<sup>2</sup> + _x_<sup>3</sup> a + _x_<sup>5</sup> _a_ <sup>3</sup>  

which you would like to evaluate on the field element _x_<sup>6</sup> over GF(8). One can use the 
evaluate() function of the field and provide information about the coefficients of the curve.
```
gf = GaloisField(2, 3, [1, 1, 0, 1])
curve = [gf[2], gf[3], 0, gf[5]]
f.evaluate(curve, gf[6]) # Should result in gf[2]
```

=============================================================================

Some functionality which has yet to be implemented is:
- Finding the self-dual basis (when possible)
- to_poly(), the companion to to_sdb(), which will switch you back to the polynomial basis.
- Matrix representations of finite field elements.

=============================================================================
Below are some commonly used irreducible polynomials, and corresponding self-dual normal bases (where applicable):

| Dimension | Polynomial | Self-dual basis |
| --------- | ---------- | --------------- |
| 4   | [1, 1, 1]                   | [1, 2] |
| 8   | [1, 1, 0, 1]                | [3, 5, 6] |
| 8   | [1, 0, 1, 1]                | [1, 2, 4] |
| 9   | [2, 1, 1]                   | No s.d. normal basis |
| 9   | [2, 2, 1]                   | No s.d. normal basis |
| 16  | [1, 1, 0, 0, 1]             | [3, 7, 12, 13]  |
| 27  | [1, 2, 0, 1]                | No s.d. normal basis |  
| 32  | [1, 0, 1, 0, 0, 1]          | [3, 5, 11, 22, 24] |
| 256 | [1, 0, 1, 1, 1, 0, 0, 0, 1] | \[5, 18, 30, 44, 106, 135, 147, 249\] (Thanks Markus!) |

=============================================================================


