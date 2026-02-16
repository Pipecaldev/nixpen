# Contributing to NixPen

Thank you for your interest in contributing to NixPen! We welcome contributions from the community to help make this the best screen annotation tool for Linux.

## How to Contribute

### Reporting Bugs
If you find a bug, please create a new issue using the **Bug Report** template. Include as much detail as possible to help us reproduce and fix the issue.

### Suggesting Enhancements
Have an idea? Open a **Feature Request** using the provided template. We love hearing how we can improve NixPen.

### Pull Requests
1.  **Fork** the repository.
2.  Create a new branch for your feature or fix:
    *   `feature/my-new-feature`
    *   `fix/bug-fix`
3.  Commit your changes following meaningful commit messages.
4.  Push to your branch.
5.  Submit a **Pull Request** to the `main` branch.

## Development Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/Pipecaldev/nixpen.git
    cd nixpen
    ```
2.  Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    python3 main.py
    ```

## Coding Standards
*   Follow PEP 8 style guidelines.
*   Keep code clean and commented where necessary.
*   Ensure existing functionality remains intact.

## License
By contributing, you agree that your contributions will be licensed under the GNU GPL v3.
