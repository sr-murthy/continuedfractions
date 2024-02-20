<div align="center">
  
[![CI](https://github.com/sr-murthy/continuedfractions/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sr-murthy/continuedfractions/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/sr-murthy/continuedfractions/graph/badge.svg?token=GWQ08T4P5J)](https://codecov.io/gh/sr-murthy/continuedfractions)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![License: MPL
2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
<a href="https://trackgit.com">
<img src="https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/lstbybzreip1xu8hdsls" alt="trackgit-views" />
</a>

</div>

# continuedfractions

A simple extension of the Python [`fractions`](https://docs.python.org/3/library/fractions.html) standard library for working with [continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) as Python objects.[^1]

## Prelude

$$
\pi = 3 + \frac{1}{7 + \frac{1}{15 + \frac{1}{1 + \frac{1}{292 + \cdots}}}}
$$

```python
>>> import decimal, math; from continuedfractions.continuedfraction import ContinuedFraction
>>> cf = ContinuedFraction(math.pi)
>>> cf
ContinuedFraction(884279719003555, 281474976710656)
>>> cf.elements
(3,7,15,1,292,1,1,1,2,1,3,1,14,4,2,3,1,12,5,1,5,20,1,11,1,1,1,2)
>>> cf.as_float()
3.141592653589793
>>> cf.convergents
mappingproxy({0: Fraction(3, 1), 1: Fraction(22, 7), 2: Fraction(333, 106), 3: Fraction(355, 113), 4: Fraction(103993, 33102), 5: Fraction(104348, 33215), 6: Fraction(208341, 66317), 7: Fraction(312689, 99532), 8: Fraction(833719, 265381), 9: Fraction(1146408, 364913), 10: Fraction(4272943, 1360120), 11: Fraction(5419351, 1725033), 12: Fraction(80143857, 25510582), 13: Fraction(325994779, 103767361), 14: Fraction(732133415, 233045304), 15: Fraction(2522395024, 802903273), 16: Fraction(3254528439, 1035948577), 17: Fraction(41576736292, 13234286197), 18: Fraction(211138209899, 67207379562), 19: Fraction(252714946191, 80441665759), 20: Fraction(1474712940854, 469415708357), 21: Fraction(29746973763271, 9468755832899), 22: Fraction(31221686704125, 9938171541256), 23: Fraction(373185527508646, 118788642786715), 24: Fraction(404407214212771, 128726814327971), 25: Fraction(777592741721417, 247515457114686), 26: Fraction(1181999955934188, 376242271442657), 27: Fraction(3141592653589793, 1000000000000000)})
>>> cf.order
27
>>> pi_approx = cf.from_elements(3, 7, 15, 1)
>>> pi_approx
ContinuedFraction(355, 113)
>>> pi_approx.as_float()
3.1415929203539825
>>> math.pi - pi_approx.as_float()
-2.667641894049666e-07
>>> import pytest
>>> pytest.approx(pi_approx.as_float(), rel=decimal.getcontext().prec) == math.pi
True
>>> ContinuedFraction('3.245')
ContinuedFraction(649, 200)
>>> (ContinuedFraction(649/200) + ContinuedFraction('-1/200'))
ContinuedFraction(81, 25)
>>> (ContinuedFraction(649, 200) - ContinuedFraction(Fraction('1/200'))).elements
(3, 4, 6)
>>> ContinuedFraction(649, 200).mediant(Fraction(-1, 200))
ContinuedFraction(81, 50)
```

## Installation & Dependencies

The package does not use any 3rd party (production) dependencies, only Python standard libraries, and is supported on Python versions `3.10`-`3.12`. It is CI-tested on Ubuntu Linux (22.04.3 LTS), Mac OS (12.7.3) and Windows (Windows Server 2022), but should also install on any other platform supporting these Python versions.

The simplest way of installing it is a standard `pip`/`pip3` install:
```python
pip install continuedfractions
```

For contributors there are development requirements which are specified in the [project TOML](pyproject.toml) - contribution guidelines are described in more detail in the [Contributing](#contributing) section.

## Working with Continued Fractions

Continued fractions are beautiful and interesting mathematical objects, with deep connections in [number theory](https://en.wikipedia.org/wiki/Number_theory) and also very useful practical applications, including the [rational approximation of real numbers](https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations).

The `continuedfractions` package is designed to make it easy to construct (finite) continued fractions as Python objects, explore their properties - elements/coefficients, convergents, segments, remainders - and operate on them as instances of the standard library [`fractions.Fraction`](https://docs.python.org/3/library/fractions.html#fractions.Fraction) class, of which they are automatically instances.

### Package Structure

The `continuedfractions` package consists of two libraries:

* [`continuedfractions.lib`](src/continuedfractions/lib.py) - this contains the core functionality of (1) generating continued fraction representations (as ordered element sequences) of any valid Python number, given as an integer, non-nan `float`, valid numeric string, a `fractions.Fraction` or `decimal.Decimal` object, or as a pair of integers and/or `fractions.Fraction` objects; and conversely (2) reconstructing rational fractions from continued fraction representations (again, given as ordered element sequences).

* [`continuedfractions.continuedFraction`](src/continuedfractions/continuedfraction.py) - this contains a simple `ContinuedFraction` class, extending from `fractions.Fraction`, which makes it possible to construct and operate on continued fractions as Python objects, and encapsulates a number of key properties, such as sequences of elements and convergents. Utility methods are also provided to compute segments, remainders, and mediants with any other `fractions.Fraction` instances.

The functions in `continuedfractions.lib` are standalone and thus useful on their own, but it is easiest to work with objects created from the `continuedfraction.ContinuedFraction` class.

### A Simple Walkthrough with Examples

From a user point of view the core package interaction should/would occur via the [`continuedfractions.continuedfraction.ContinuedFraction`](src/continuedfraction.py) class. An example walkthrough is given below illustrating how to use it.

### Importing the `ContinuedFraction` Class

Import the core class (inserting `'src'` into `sys.path` beforehand, if necessary) from `continuedfractions.continuedfraction`.
```python
>>> from continuedfractions.continuedfraction import ContinuedFraction
```

### Creating Continued Fractions from Numbers

We start with the rational number[^2] $`\frac{649}{200} = \frac{600 + 49}{200} = 3.245`$, which has the following finite, unique simple continued fraction representation:

$$
\frac{649}{200} = 3 + \frac{4}{1 + \frac{12}{1 + \frac{1}{4}}}
$$

We can construct the continued fraction object for $\frac{649}{200}$ as follows.

```python
>>> cf = ContinuedFraction(649, 200)
>>> cf
ContinuedFraction(649, 200)
```

**Note**: The same object can also be constructed using `ContinuedFraction('649/200')`, `ContinuedFraction('3.245')`, `ContinuedFraction(Fraction(649, 200))`, `ContinuedFraction((649), 200))`, `ContinuedFraction(649, Fraction(200)))`, and `ContinuedFraction(Decimal('3.245'))`. But passing a numeric literal such as `649/200` will result in an evaluation of the decimal integer division using binary floating point division, thus producing a fractional approximation, in this case, `ContinuedFraction(3653545197704315, 1125899906842624)`.

The float value of `ContinuedFraction(649, 200)` is available via the `.as_float()` method.

```python
>>> cf.as_float()
3.245
```

### Inspecting Properties


A number of interesting properties of (finite) continued fractions can be explored using `ContinuedFraction`, as described below.

#### Elements and Orders

The (ordered) sequence of **elements** (or coefficients) of this continued fraction object, which is written mathematically as $[3; 4, 12, 4]$ in modern notation, can be obtained via the `.elements` property.

```python
>>> cf.elements
(3, 4, 12, 4)
```

**Note**: The continued fraction representation given above is called "simple", because the last element is always a positive integer $> 1$.[^3]

The elements $a_0,a_1,...$ of a continued fraction representation of a real number $x$, which we may assume is positive, consist of the number $\lfloor x \rfloor = a_0$ and the whole number parts of the denominators of the reciprocals in the representation.

The **order** of a continued fraction is defined to be number of its elements **after** the first. Thus, for $\frac{649}{200}$ we can verify that it is indeed $3$, using the `.order` property.

```python
>>> cf.order
3
```

#### Convergents

For a non-negative integer $k > 0$ the $k$-th **convergent** of a (possibly infinite) continued fraction represented by $[a_0, a_1,\ldots]$ is defined to be the rational number and finite continued fraction represented by $[a_0, a_1,\ldots,a_k]$, which is formed from the first $k + 1$ elements of the original. The convergents have the property that they form a strictly increasing sequence of rational numbers which is bounded by and converges to a real number $x$ - each convergent represents a closer / better rational approximation to $x$ than the previous one.

The `ContinuedFraction` class provides a `.convergents` property for objects, which returns an immutable map ([`types.MappingProxyType`](https://docs.python.org/3/library/types.html#types.MappingProxyType)) of all $k$-order convergents, indexed or keyed by integers $k=0,1,\ldots,n$, where $n$ is the (finite) order of the continued fraction.

```python
>>> cf.convergents
mappingproxy({0: Fraction(3, 1), 1: Fraction(13, 4), 2: Fraction(159, 49), 3: Fraction(649, 200)})
>>> cf.convergents[2]
Fraction(159, 49)
>>> assert cf.convergents[0] < cf.convergents[1] < cf.convergents[2] < cf.convergents[3]
# True
```

**Note**: As the convergents are determined during `ContinuedFraction` object initialisation, the objects that represent them cannot be of type `ContinuedFraction`, due to recursion errors. Thus, it was decided to keep them as `fractions.Fraction` objects.


#### Segments and Remainders

Convergents are linked to the concept of **segments**, which are finite subsequences of elements of a given continued fraction. More precisely, we can define the $k$-th segment of a continued fraction represented by $[a_0, a_1,\ldots]$ as the sequence of its first $k + 1$ elements, namely $a_0,a_1,\ldots,a_k$, which uniquely determines the $k$-order convergent of the continued fraction. The segments of `ContinuedFraction` objects can be obtained via the `.segment()` method, which takes a non-negative integer not exceeding the order.


```python
>>> cf.segment(0), cf.segment(1), cf.segment(2), cf.segment(3)
(ContinuedFraction(3, 1), ContinuedFraction(13, 4), ContinuedFraction(159, 49), ContinuedFraction(649, 200))3
```
**Note**: Unlike the $k$-order convergents the segments are `ContinuedFraction` objects and uniquely represent them as such.

A related concept is that of **remainders** of continued fractions, which are (possibly infinite) subsequences of elements of a given continued fraction, starting a given element. More precisely, we can define the $k$-th remainder of a continued fraction represented by $[a_0, a_1,\ldots]$ as the sequence of elements $a_k,a_{k + 1},\ldots$ starting from the $k$-th element. The remainders of `ContinuedFraction` objects can be obtained via the `.remainder()` method, which takes a non-negative integer not exceeding the order.

```python
>>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
(ContinuedFraction(649, 200), ContinuedFraction(200, 49), ContinuedFraction(49, 4), ContinuedFraction(4, 1))
```

An another interesting feature which the package includes is [mediants](https://en.wikipedia.org/wiki/Mediant_(mathematics)). The mediant of two fractions $\frac{a}{b}$ and $\frac{c}{d}$, where $b, d > 0$, is given by the fraction:

$$
\frac{a + c}{b + d}
$$

It has a number of interesting properties, including the inequality:

$$
\frac{a}{b} < \frac{a + c}{b + d} < \frac{c}{d}
$$

The `ContinuedFraction` class provides a `.mediant()` method for objects to compute their mediants with a given fraction, which could be another `ContinuedFraction` or `fractions.Fraction` object. A few examples are given below.


```python
>>> ContinuedFraction('0.5').mediant(Fraction(2, 3))
>>> ContinuedFraction(3, 5)
>>> ContinuedFraction(1, 2).mediant(ContinuedFraction('2/3'))
>>> ContinuedFraction(3, 5)
>>> assert ContinuedFraction(1, 2) < ContinuedFraction(1, 2).mediant(1) < 1
# True

````

### Constructing Continued Fractions from Element Sequences

Continued fractions can also be constructed from element sequences, using the `ContinuedFraction.from_elements()` class method, and as a subclass of `fractions.Fraction` all `ContinuedFraction` objects are fully operable as rational numbers, and including as negative rationals.
```python
>>> cf_inverse = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
>>> cf_inverse
ContinuedFraction(200, 649)
>>> cf_inverse.elements
(0, 3, 4, 12, 4)
>>> assert cf_inverse == 1/cf
# True
>>> assert cf * cf_inverse == 1
# True
>>> cf_negative_inverse = ContinuedFraction.from_elements(-1, 1, 2, 4, 12, 4)
>>> cf_negative_inverse
ContinuedFraction(-200, 649)
>>> cf_negative_inverse.elements
(-1, 1, 2, 4, 12, 4)
>>> assert cf_negative_inverse == -1/cf
# True
>>> assert cf * cf_negative_inverse == -1
>>> assert cf + (-cf) == cf_inverse + cf_negative_inverse == 0
# True
```

"Negative" continued fractions are supported but for attribute accesss to work the minus sign must be attached to the fraction, before enclosure in parentheses.
```python
>>> -cf.elements
...
TypeError: bad operand type for unary -: 'tuple'
>>> -(cf).elements
...
TypeError: bad operand type for unary -: 'tuple'
>>> (-cf).elements
(-4, 1, 3, 12, 4)
>>> assert cf + (-cf) == 0
# True
```

Finally, it should be noted that `ContinuedFraction` validates all inputs during object creation (`.__new__()` class method) - not initialisation - using the `.validate()` class method. Any inputs that do not meet the following conditions trigger `ValueError`.

* a single integer or a non-nan float
* a single numeric string
* a single `fractions.Fraction` or `decimal.Decimal` object
* two integers or `fractions.Fraction` objects, or a combination of an integer and a `fractions.Fraction` object, representing the numerator and non-zero denominator of a rational fraction

A number of examples are given below of validation passes and fails.
```python
>>> ContinuedFraction.validate(100)
>>> ContinuedFraction.validate(3, -2)

>>> ContinuedFraction.validate(1, -2.0)
Traceback (most recent call last):
...
ValueError: Only single integers, non-nan floats, numeric strings, 
`fractions.Fraction`, or `decimal.Decimal` objects; or two 
integers or two `fractions.Fraction` objects or a pairwise 
combination of these, representing the numerator and non-zero 
denominator, respectively, of a rational fraction, are valid.

>>> ContinuedFraction.validate(-.123456789)
>>> ContinuedFraction.validate('-.123456789')
>>> ContinuedFraction.validate('-649/200')
>>> ContinuedFraction.validate(-3/2)

>>> ContinuedFraction.validate(-3, 0)
Traceback (most recent call last):
...
ValueError: Only single integers, non-nan floats, numeric strings, 
`fractions.Fraction`, or `decimal.Decimal` objects; or two 
integers or two `fractions.Fraction` objects or a pairwise 
combination of these, representing the numerator and non-zero 
denominator, respectively, of a rational fraction, are valid.

>>> ContinuedFraction.validate(Fraction(-415, 93))
>>> ContinuedFraction.validate(Decimal('12345.6789'))
>>> ContinuedFraction.validate(Decimal(12345.6789))

>>> ContinuedFraction.validate(Fraction(3, 2), 2.5)
Traceback (most recent call last):
...
ValueError: Only single integers, non-nan floats, numeric strings, 
`fractions.Fraction`, or `decimal.Decimal` objects; or two 
integers or two `fractions.Fraction` objects or a pairwise 
combination of these, representing the numerator and non-zero 
denominator, respectively, of a rational fraction, are valid.
````

## Contributing

Contributors and contributions are welcome via pull requests from a fork targeting the parent [`main` branch](https://github.com/sr-murthy/continuedfractions/tree/main). As this is a new and fairly specialised project a simple Git workflow, using a feature and/or fix branch created off the `main` branch of your fork, is recommended.

### SSH and Cloning

If you wish to contribute please first ensure you have [SSH access to GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh). If you do then this should work:
```bash
ssh -vT git@github.com
```

If not please follow the SSH instructions linked above. This should include ensuring that your SSH config file defines your SSH private key file, and specifies agent forwarding, and public key authentication as the preferred mode. For Linux and Mac OS users the file should look like something below.

```bash
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  ForwardAgent yes
  Preferredauthentications publickey
  IdentityFile /path/to/your/ssh/private/keyfile
  PasswordAuthentication no
```

Once you've forked the repository, it is recommended to clone your fork over SSH:

```python
git clone git+ssh://git@github.com/<fork user>/continuedfractions
```

### Dependencies & PDM

As mentioned earlier, the package has no (production) dependencies, but groups of development requirements are specified in the `[tool.pdm.dev-dependencies]` section of the [project TOML](pyproject.toml). Of these only the `test` dependencies, including [`pytest`](https://docs.pytest.org/en/8.0.x/) and [`pytest-cov`](https://pytest-cov.readthedocs.io/), are important.

```toml
test = [
    "coverage[toml]",
    "pytest",
    "pytest-cov",
    "pytest-xdist",
]
```

[PDM](https://pdm-project.org/latest) is used (by myself, currently, the sole maintainer) to manage all dependencies and publish packages to PyPI. It is also used to automate certain tasks, such as running tests, as described in the section.

There are no `requirements*.txt` files - however, a [PDM lockfile](`pdm.lock`) which defines metadata for all TOML-defined development dependencies, including the currently empty set of production dependencies, and their sub-dependencies etc., can be used to install the project in editable mode.

```bash
pdm install -v
```

### Makefile and Tests

The [`Makefile`](Makefile) defines two main targets: `doctests` for running [doctests](https://docs.python.org/3/library/doctest.html) and `unittests` for running unittests and measuring coverage, using `pytest` and `pytest-cov`:

```bash
make doctests
make unittests
```

The doctests serve as acceptance tests, and should be run first, before the unit tests.

### Continous Integration and Deployment (CI/CD)

TODO

### Versioning & Package Publishing

TODO

## License

The project is [licensed](LICENSE) under the [Mozilla Public License 2.0](https://opensource.org/licenses/MPL-2.0).


## References

[1] Barrow, John D. “Chaos in Numberland: The secret life of continued fractions.” plus.maths.org, 1 June 2000, https://plus.maths.org/content/chaos-numberland-secret-life-continued-fractionsURL.

[2] Emory University Math Center. “Continued Fractions.” The Department of Mathematics and Computer Science, https://mathcenter.oxford.emory.edu/site/math125/continuedFractions/. Accessed 19 Feb 2024.

[3] Wikipedia. "Continued Fraction". https://en.wikipedia.org/wiki/Continued_fraction. Accessed 19 February 2024.

[^1]: Due to the nature of [binary floating point arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html) it is not always possible to exactly represent a given [real number](https://en.wikipedia.org/wiki/Real_number). For the same reason, the continued fraction representations produced by the package will necessarily be [finite](https://en.wikipedia.org/wiki/Continued_fraction#Finite_continued_fractions).

[^2]: The definition of "rational number" used here is standard: an irreducible ratio $\frac{a}{b}$ of integers $a$ and $b \neq 0$.

[^3]: See any reference on finite continued fractions, e.g. https://en.wikipedia.org/wiki/Continued_fraction#Finite_continued_fractions.