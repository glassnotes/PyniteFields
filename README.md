# PyniteFields
A class library for operations on finite fields (a.k.a. Galois fields) which I find useful in my line of work.

PyniteFields is meant to be fairly intuitive and easy to use. It's inspired by some of the ideas in the Mathematica
FiniteFields package, which is pretty great (except then you have to write everything _else_ in Mathematica too).

All operations are done with a single object of the class GaloisField. 

You can create a field with prime order like so (using order 5):
```
gf = GaloisField(5)
```

To create a field with power of prime order you'll need 3 things:
- A base prime _p_,
- An exponent _n_ such that the field has order _p<sup>n</sup>_,
- Coefficients for an irreducible polynomial with degree _n_.

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
gf[2]   # Returns the element _x_<sup>2</sup>
gf[0]   # Returns the first element (i.e. 0)
gf[p - 1]   # Returns the last element, which is always 1
```

Field elements are stored as lists of coefficients in the polynomial basis. For primes this
is very simple - the polynomial basis is just 1, so we store the elements themselves in a 
single item list. For power of primes, let's go back
to our example of dimension 8. Element _x<sup>3</sup>_ can be expressed as 1 + _x_, so 
it is stored as the list [1, 1, 0].

We can sum, subtract, multiply field elements, and take their power:
```
gf[3] + gf[5]
gf[2] - gf[7]
gf[4] * gf[1]
pow(gf[4], 3)
```

We can also take the trace, which is quite a useful operation:
```
gf[2].trace()
``` 

Some functionality which has yet to be implemented is:
- Finding the self-dual basis (when possible)
- Transforming the field such that the elements are expressed in the self-dual basis

