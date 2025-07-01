<div align="center">
  
[![CI](https://github.com/sr-murthy/continuedfractions/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sr-murthy/continuedfractions/actions/workflows/ci.yml)
[![CodeQL Analysis](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml)
[![Codecov](https://codecov.io/gh/sr-murthy/continuedfractions/graph/badge.svg?token=GWQ08T4P5J)](https://codecov.io/gh/sr-murthy/continuedfractions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
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
https://camo.githubusercontent.com/bb88127790fb054cba2caf3f3be2569c1b97bb45a44b47b52d738f8781a8ede4/68747470733a2f2f696d672e736869656c64732e696f2f656e64706f696e743f75726c3d68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f636861726c6965726d617273682f727566662f6d61696e2f6173736574732f62616467652f76312e6a736f6e
# continuedfractions

A simple extension of the Python [`fractions`](https://docs.python.org/3/library/fractions.html) standard library for working with (finite, simple) [continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) as Python objects.

Install from [PyPI](https://pypi.org/project/continuedfractions/):
```shell
pip install -U continuedfractions
```
or the `main` branch of this repo:
```shell
pip install -U git+https://github.com/sr-murthy/continuedfractions
```

See the [project docs](https://continuedfractions.readthedocs.io) for more details, which includes the [API reference](https://continuedfractions.readthedocs.io/sources/api-reference.html).

[Continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) are beautiful and interesting mathematical objects, with many connections in [number theory](https://en.wikipedia.org/wiki/Number_theory) and also very useful practical applications, including the [rational approximation of real numbers](https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations).

The `continuedfractions` package is designed for users interested in:

* learning about and working with (finite, simple) continued fractions as Python objects, in an intuitive object-oriented way
* exploring their key properties, such as elements/coefficients, convergents, semiconvergents, remainders, and others
* operating on them as rationals and instances of the standard library [`fractions.Fraction`](https://docs.python.org/3/library/fractions.html#fractions.Fraction) class
* making approximations of and experimental computations for irrational numbers
* exploring other related objects, such as mediants, and special sequences of rational numbers such as Farey sequences

The project is [licensed](LICENSE) under the [Mozilla Public License 2.0](https://opensource.org/licenses/MPL-2.0).
