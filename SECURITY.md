# Security Policy

## Supported Versions

The package currently only uses Python standard libraries (see the [project TOML](https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml)), and has no 3rd party dependencies. Security / vulnerability alerts related to [Python itself](https://www.cvedetails.com/vulnerability-list/vendor_id-10210/product_id-18230/Python-Python.html) would be addressed within Python.

A listing of current security / vulnerability alerts is available via [Dependabot alerts](https://github.com/sr-murthy/continuedfractions/security) - these are usually related to sub-dependencies of optional or development dependencies, and are addressed via dedicated PRs as they arise.

The repository is enabled with a number of features to ensure security, including [CodeQL analysis](https://github.com/sr-murthy/continuedfractions/actions/workflows/codeql-analysis.yml), 
[Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) and [secrets scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning).

## Reporting a Vulnerability

Any vulnerability that could potentially impact the installation or performance of the package, or the accuracy of its results in computations, should be reported privately via email to the maintainer: [s.murthy@tutanota.com](s.murthy@tutanota.com).
