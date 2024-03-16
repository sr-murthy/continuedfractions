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
[![PyPI version](https://badge.fury.io/py/continuedfractions.svg)](https://badge.fury.io/py/continuedfractions)
[![Downloads](https://static.pepy.tech/badge/continuedfractions/week)](https://pepy.tech/project/continuedfractions)

</div>

# continuedfractions

A simple extension of the Python [`fractions`](https://docs.python.org/3/library/fractions.html) standard library for working with [continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) as Python objects.

The [PyPI package](https://pypi.org/project/continuedfractions/) only uses standard libraries and can be installed on any **Linux**, **Mac OS** or **Windows** system supporting **Python 3.10**, **3.11**, or **3.12**.
```shell
pip install continuedfractions
```

See the [project docs](https://continuedfractions.readthedocs.io/en/latest) for more details.

[Continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) are beautiful and interesting mathematical objects, with many connections in [number theory](https://en.wikipedia.org/wiki/Number_theory) and also very useful practical applications, including the [rational approximation of real numbers](https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations).

The `continuedfractions` package is designed to:

* make it easy to construct (finite) continued fractions as Python objects
* explore their key properties, such as elements/coefficients, convergents, segments, remainders, and others
* operate on them as rationals and instances of the standard library [`fractions.Fraction`](https://docs.python.org/3/library/fractions.html#fractions.Fraction) class

The project is [licensed](LICENSE) under the [Mozilla Public License 2.0](https://opensource.org/licenses/MPL-2.0).


