<div align="center">
  
[![CI](https://github.com/sr-murthy/continuedfractions/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sr-murthy/continuedfractions/actions/workflows/ci.yml)
[![CodeQL Analysis](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml)
[![Codecov](https://codecov.io/gh/sr-murthy/continuedfractions/graph/badge.svg?token=GWQ08T4P5J)](https://codecov.io/gh/sr-murthy/continuedfractions)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![License: MPL
2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Docs](https://readthedocs.org/projects/continuedfractions/badge/?version=latest)](https://continuedfractions.readthedocs.io/en/latest/?badge=latest)
<a href="https://trackgit.com">
<img src="https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/lsudelfvcxb7f1xm6i4l" alt="trackgit-views" />
</a>
[![PyPI version](https://img.shields.io/pypi/v/continuedfractions?logo=python&color=41bb13)](https://pypi.org/project/continuedfractions)
[![Downloads](https://static.pepy.tech/badge/continuedfractions)](https://pepy.tech/project/continuedfractions)

</div>

# continuedfractions

A simple extension of the Python [`fractions`](https://docs.python.org/3/library/fractions.html) standard library for working with [continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) as Python objects.

The [PyPI package](https://pypi.org/project/continuedfractions/) is updated as necessary with improvements, features and fixes. Only standard libraries are used, and the package can be installed on any **Linux**, **Mac OS** or **Windows** system supporting **Python 3.10**, **3.11**, or **3.12**.
```shell
pip install continuedfractions
```

See the [project docs](https://continuedfractions.readthedocs.io/en/latest/) for more details, which includes the [API reference](https://continuedfractions.readthedocs.io/en/latest/sources/api-reference.html).

[Continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) are beautiful and interesting mathematical objects, with many connections in [number theory](https://en.wikipedia.org/wiki/Number_theory) and also very useful practical applications, including the [rational approximation of real numbers](https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations).

The `continuedfractions` package is designed for users interested in:

* learning about and working with (finite) continued fractions as Python objects, in an intuitive object-oriented way
* exploring their key properties, such as elements/coefficients, convergents, semiconvergents, remainders, and others
* operating on them as rationals and instances of the standard library [`fractions.Fraction`](https://docs.python.org/3/library/fractions.html#fractions.Fraction) class
* making approximations of and experimental computations for irrational numbers
* exploring other related objects, such as mediants, and special sequences of rational numbers such as Farey sequences

Currently, it does **not** support the following features:

* infinite and generalised continued fractions
* symbolic representations of or operations with continued fractions

These are [planned](https://github.com/sr-murthy/continuedfractions/issues) for future releases.

The project is [licensed](LICENSE) under the [Mozilla Public License 2.0](https://opensource.org/licenses/MPL-2.0).


