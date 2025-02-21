# Contributing to Darkelf Browser

Thank you for your interest in contributing to Darkelf Browser! Your contributions help make this project better for everyone. Here are some guidelines to help you get started.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Submitting Pull Requests](#submitting-pull-requests)
3. [Development Setup](#development-setup)
4. [Style Guides](#style-guides)
   - [Git Commit Messages](#git-commit-messages)
   - [Python Style Guide](#python-style-guide)
5. [License](#license)

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the behavior we expect from contributors.

## How to Contribute

### Reporting Bugs

If you find a bug in the project, please create an issue in the [issue tracker](https://github.com/Darkelf2024/Darkelf-Browser/issues) and include the following information:

- A clear and descriptive title
- Steps to reproduce the problem
- Expected and actual behavior
- Screenshots, if applicable
- Any relevant logs or error messages

### Suggesting Features

We welcome feature suggestions! To suggest a feature, please create an issue in the [issue tracker](https://github.com/Darkelf2024/Darkelf-Browser/issues) and include the following information:

- A clear and descriptive title
- A detailed description of the proposed feature
- Any examples or use cases

### Submitting Pull Requests

To submit a pull request, follow these steps:

1. Fork the repository and clone your fork.
2. Create a new branch from `main` for your changes.
3. Make your changes, ensuring that your code follows the project's [style guides](#style-guides).
4. Commit your changes with a clear and descriptive commit message.
5. Push your branch to your fork.
6. Open a pull request in the main repository, describing your changes and referencing any related issues.

Please make sure your pull request passes all tests and includes any necessary documentation updates.

## Development Setup

To set up your development environment, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Darkelf2024/Darkelf-Browser.git
   cd Darkelf-Browser
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Make sure all tests pass:

   ```bash
   pytest
   ```

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally.

### Python Style Guide

Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Use [Black](https://github.com/psf/black) to format your code:

```bash
black .
```

## License

By contributing to Darkelf Browser, you agree that your contributions will be licensed under the [MIT License](LICENSE).
