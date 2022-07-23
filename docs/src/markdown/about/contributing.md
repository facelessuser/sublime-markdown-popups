# Contributing &amp; Support

## Overview

Sublime Versions | Description
-----------------|------------
ST3              | Fully supported and actively maintained.

Contribution from the community is encouraged and can be done in a variety of ways:

- Bug reports.
- Reviewing code.
- Code patches via pull requests.
- Documentation improvements via pull requests.

## Become a Sponsor :octicons-heart-fill-16:{: .heart-throb}

Open source projects take time and money. Help support the project by becoming a sponsor. You can add your support at
any tier you feel comfortable with. No amount is too little. We also accept one time contributions via PayPal.

[:octicons-mark-github-16: GitHub Sponsors](https://github.com/sponsors/facelessuser){: .md-button .md-button--primary }
[:fontawesome-brands-paypal: PayPal](https://www.paypal.me/facelessuser){ .md-button}

## Bug Reports

1. Please **read the documentation** and **search the issue tracker** to try to find the answer to your question **before** posting an issue.

2. When creating an issue on the repository, please provide as much info as possible:

    - Sublime Text build.
    - Operating system.
    - Errors in console.
    - Color scheme currently being used.
    - Language syntax highlighter being used if issue deals with a code highlighting.
    - Detailed description of the problem.
    - Examples for reproducing the error.  You can post pictures, but if specific text or code is required to reproduce the issue, please provide the text in a plain text format for easy copy/paste.

    The more info provided the greater the chance someone will take the time to answer, implement, or fix the issue.

3. Be prepared to answer questions and provide additional information if required.  Issues in which the creator refuses to respond to follow up questions will be marked as stale and closed.

## Reviewing Code

Take part in reviewing pull requests and/or reviewing commits and merges.  Make suggestions to improve the code and discuss solutions to overcome weakness in the algorithm.

## Pull Requests

Pull requests are welcome, and if you plan on contributing directly to the code, there are a couple of things to be mindful of.

1. Please describe the change in as much detail as possible so I can understand what is being added or modified.

2. If you are solving a bug that does not already have an issue, please describe the bug in detail and provide info on how to reproduce if applicable (this is good for me and others to reference later when verifying the issue has been resolved).

3. Please reference and link related open bugs or feature requests in this pull if applicable.

4. Make sure you've documented or updated the existing documentation if introducing a new feature or modifying the behavior of an existing feature that a user needs to be aware of.  I will not accept new features or changes to existing features if you have not provided documentation describing the feature.

Continuous integration tests on are run on all pull requests and commits via Travis CI.  When making a pull request, the tests will automatically be run, and the request must pass to be accepted.  You can (and should) run these tests before pull requesting.  If it is not possible to run these tests locally, they will be run when the pull request is made, but it is strongly suggested that requesters make an effort to verify before requesting to allow for a quick, smooth merge.

### Running Validation Tests

Linting is performed on the entire project with the following modules:

  - @gitlab:pycqa/flake8
  - @gitlab:pycqa/flake8-docstrings
  - @ebeweber/flake8-mutable
  - @gforcada/flake8-builtins
  - @gitlab:pycqa/pep8-naming

These can be installed via:

```
pip install flake8
pip install flake8-docstrings
pip install flake8-mutable
pip install flake8-builtins
pip install pep8-naming
```

Linting is performed with the following command:

```
flake8 .
```

## Documentation Improvements

A ton of time has been spent not only creating and supporting this plugin, but also spent making this documentation.  If you feel it is still lacking, show your appreciation for the plugin by helping to improve the documentation.  Help with documentation is always appreciated and can be done via pull requests.  There shouldn't be any need to run validation tests if only updating documentation.

You don't have to render the docs locally before pull requesting, but if you wish to, I currently use a combination of @mkdocs/mkdocs, the @squidfunk/mkdocs-material, and @facelessuser/pymdown-extensions to render the docs.  You can preview the docs if you install these two packages.  The command for previewing the docs is `mkdocs serve` from the root directory. You can then view the documents at `localhost:8000`.
