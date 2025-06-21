# Contributing Guide

Thank you for considering contributing to AudioBookzOrganizer!

## Reporting Bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) to provide a clear description and steps to reproduce.

## Development Setup

1. Install the project with test dependencies:
   ```bash
   pip install -e .[test]
   ```
2. Run the tests:
   ```bash
   pytest
   ```
3. Lint the code:
   ```bash
   ruff check .
   ```

## Pull Requests

* Create a feature branch from `main`.
* Ensure tests and linting pass.
* Submit a pull request describing your changes.
