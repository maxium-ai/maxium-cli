# Contributing

Welcome to Maxium CLI! Here's how to get started.

## Quick Start

```bash
# Fork and clone
git clone git@github.com:your-username/maxium-cli.git
cd maxium-cli

# Install dependencies and pre-commit hooks
pip install -e ".[dev]"
pre-commit install

# Create feature branch and develop
gx create feature-name
pytest tests/
gx push
```

## Development Setup

We use pre-commit hooks to maintain code quality:
- Code formatting with Black (88 char limit)
- Import sorting with isort
- Type checking
- Docstring validation

The hooks run automatically on commit. Run manually with:
```bash
pre-commit run --all-files
```

## Pull Request Process

1. Ensure all pre-commit hooks and tests pass
2. Submit PR with:
   - Clear title and description
   - Issue references
   - Screenshots for UI changes
   - Changelog entry under "Unreleased"

## Need Help?

- Open an issue for questions and we will respond ⚡️blazingly fast⚡️