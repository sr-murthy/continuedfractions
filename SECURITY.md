# Security Policy

## Supported Versions

The package currently only uses Python standard libraries (see the [project TOML](https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml)), and has no 3rd party dependencies. Therefore the only security / vulnerability alerts that are relevant relate to [Python itself](https://www.cvedetails.com/vulnerability-list/vendor_id-10210/product_id-18230/Python-Python.html), which would be addressed by the Python core development team.

Future addition of 3rd party dependencies would change the situation, and in that case at least the latest (minor) version of the package would receive and support security updates.

Also note that the repository is enabled with a number of features to ensure security, including [CodeQL analysis](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml), 
[Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) and [secrets scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning).

## Reporting a Vulnerability

Any vulnerability that could potentially impact the installation or performance of the package, or the accuracy of its results in computations, should be reported privately via email to the maintainer: [s.murthy@tutanota.com](s.murthy@tutanota.com).
