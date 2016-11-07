A short tutorial on PyniteFields
********************************

The basics
=============

This tutorial assumes basic knowledge of finite fields. If you need a refresher,
I have a short set of notes here on my webpage, or there are many fantastic
textbooks that will cover the basics.

Once you've installed PyniteFields, all you need to do to get going is to 
create an object of type GaloisField.

You can create a Galois field with prime order, :math:`\text{GF}(p)`, 
like so (using order 5).::

    from pynitefields import * 
    gf = GaloisField(5)

To create a field with power of prime order you'll need 3 things:

* A base prime :math:`p`
* An exponent :math:`n` such that the field has order :math:`p^n`
* A primitive, irreducible polynomial of degree :math:`n` over the base field :math:`\text{GF}(p)`.

For example, suppose we want to create the field GF(8). We know the irreducible 
polynomial :math:`1 + x + x^3`, so we put it's coefficients into a list: 
[1, 1, 0, 1]. The :math:`i`'th entry in the list corresponds to the 
coefficient attached to the :math:`i`'th power.

To create the prime power field (using 8 as our example) we feed it the prime, 
exponent and coefficients in order.::

   gf = GaloisField(2, 3, [1, 1, 0, 1])

All subsequent operations can be achieved using the object ``gf`` which 
we have created.

We can grab the :math:`i`'th power of the primitive element 
using the [] operator.::

    gf[0]   # Returns the first element (i.e. 0)
    gf[2]   # Returns the element x^2
    gf[p^n - 1]  # Returns the last element of the field

Field elements are stored as lists of coefficients in the polynomial basis. 
For primes this is very simple - the polynomial basis is just 1, so we store 
the elements themselves in a single item list. For power of primes, 
let's go back to our example of dimension 8. Element :math:`x^3` can be 
expressed as :math:`1 + x`, so it is stored as the list ``[1, 1, 0]``.

Operations on field elements
============================

We can perform all four arithmetic operations on field elements, and take 
their powers and inverses.::

    gf[3] + gf[5]
    gf[2] - gf[7]
    gf[4] * gf[1]
    gf[1] / gf[6]
    pow(gf[4], 3)
    inv(gf[2])

Note that by convention, we take the 0'th power of the primitive element to be 0.

We can also take the trace, which is quite a useful operation. It is expressed
as

.. math::

    \text{tr}({\alpha}) = {\alpha} + {\alpha}^p + \cdots + {\alpha}^{p^(n-1)}

The result of the trace is always an element of the base field, 
:math:`\text{GF}(p)`. It can be invoked programatically in two ways.::

    gf[2].tr()
    tr(gf[2])  # Same as above, but more convenient to write

We also implement a group character for the finite field. For this, we must 
make use of the pth root of unity, 

.. math::

    \omega_p = \exp \left( \frac{2 \pi i}{p} \right).

The :math:`\omega_p` are implemented in a separate class pthRootOfUnity. Then,
we define the group character as

.. math::
    
    \chi({\alpha}) = \omega_{p}^{\text{tr}({\alpha})} 

For qubit systems, the character will be :math:`\pm1`. For qudit systems, it 
will be some power of :math:`\omega_p`. Like the trace, it can be called in
two ways:::

    gf[3].gchar()
    gchar(gf[3])  


Changing bases
==============

It is possible to convert the field such that all the elements are 
expanded in terms of a self-dual normal basis rather than the polynomial basis. 
The characteristic of a self-dual normal basis is that

.. math::

    \text{tr}({\theta_i} {\theta_j}) = \delta_{ij}

for any two basis elements :math:`\theta_i, \theta_j`.

For example, suppose we are working in GF(4). The elements :math:`x` and 
:math:`x^2` comprise a self-dual basis. To convert the field we can do::

    gf = GaloisField(2, 2, [1, 1, 1])
    gf.to_sdb([1, 2])

Currenty, the program does not compute a self-dual basis for you - you will 
have to provide one yourself. Here, ``to_sdb`` takes as an argument a 
list of powers of the primitive element which make up the self-dual basis. 
For more examples, see the table at the end of this document.

Curves
======

PyniteFields can evaluate functions, or curves, over field elements. 
Suppose you have some function  

.. math::
 
    {\beta}({\alpha}) = x^2 + x^3 {\alpha} + x^5 {\alpha}^3

which you would like to evaluate on the field element :math:`x^6` over GF(8). 
One can use the evaluate() function of the field and provide information 
about the coefficients of the curve.::

    gf = GaloisField(2, 3, [1, 1, 0, 1])
    curve = [gf[2], gf[3], 0, gf[5]]
    gf.evaluate(curve, gf[6]) # Should result in gf[2]

This functionality is used by Balthasar's Curve class. In general, for a curve
:math:`{\beta}({\alpha}) = c_0 + c_1 {\alpha} + \ldots + c_k {\alpha}^k`,
we should feed ``evaluate`` a curve which has list form 
:math:`[c_0, c_1, \ldots, c_k]`. Note that for coefficients which are 
essentially integers, you can simply put the integer rather
than specifying it as a field element (e.g. [f[1], f[2], 2]).

Future functionality
=============================================================================

Some functionality which has yet to be implemented is:

* Finding the self-dual basis (when possible)
* to_poly(), the companion to to_sdb(), which will switch you back to the polynomial basis.
* Matrix representations of finite field elements.

Useful data
==========================
Below are some commonly used irreducible polynomials, and 
corresponding self-dual normal bases (where applicable):

+-----------+-----------------------------+------------------------------------------------------+
| Dimension | Polynomial                  | Self-dual basis                                      |
+===========+=============================+======================================================+
| 4         | [1, 1, 1]                   | [1, 2]                                               |
+-----------+-----------------------------+------------------------------------------------------+
| 8         | [1, 1, 0, 1]                | [3, 5, 6]                                            |
+-----------+-----------------------------+------------------------------------------------------+
| 8         | [1, 0, 1, 1]                | [1, 2, 4]                                            |
+-----------+-----------------------------+------------------------------------------------------+
| 9         | [2, 1, 1]                   | No s.d. normal basis                                 |
+-----------+-----------------------------+------------------------------------------------------+
| 9         | [2, 2, 1]                   | No s.d. normal basis                                 |
+-----------+-----------------------------+------------------------------------------------------+
| 16        | [1, 1, 0, 0, 1]             | [3, 7, 12, 13]                                       |
+-----------+-----------------------------+------------------------------------------------------+
| 27        | [1, 2, 0, 1]                | No s.d. normal basis                                 |  
+-----------+-----------------------------+------------------------------------------------------+
| 32        | [1, 0, 1, 0, 0, 1]          | [3, 5, 11, 22, 24]                                   |
+-----------+-----------------------------+------------------------------------------------------+
| 256       | [1, 0, 1, 1, 1, 0, 0, 0, 1] | [5, 18, 30, 44, 106, 135, 147, 249] (Thanks Markus!) |
+-----------+-----------------------------+------------------------------------------------------+

