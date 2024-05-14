# Security Policy

## Supported Versions

The package currently only uses Python standard libraries (see the [project TOML](https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml)), and has no 3rd party dependencies. Therefore the only security / vulnerability alerts that are relevant relate to [Python itself](https://www.cvedetails.com/vulnerability-list/vendor_id-10210/product_id-18230/Python-Python.html), which would be addressed within Python itself.

If 3rd party dependencies are added there may be security patches applied as and when needed.

The repository is enabled with a number of features to ensure security, including [CodeQL analysis](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml), 
[Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) and [secrets scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning).

## Reporting a Vulnerability

Any vulnerability that could potentially impact the installation or performance of the package, or the accuracy of its results in computations, should be reported privately via email to the maintainer: [s.murthy@tutanota.com](s.murthy@tutanota.com).
