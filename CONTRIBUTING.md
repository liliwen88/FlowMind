# Contributing to llm-flow-dsl

Thank you for your interest in contributing to llm-flow-dsl! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/llm-flow-dsl.git
   cd llm-flow-dsl
   ```
3. **Install** development dependencies:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Before You Start

- Check open issues and pull requests to avoid duplicate work
- Create an issue to discuss major changes before starting work
- Follow the Code of Conduct in all interactions

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b fix/your-fix-name
   # or
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear commit messages:
   ```bash
   git commit -m "Fix: descriptive message about what you changed"
   ```

3. **Add tests** for your changes:
   - All new features must have tests
   - Bug fixes should include a test that reproduces the issue
   - Run tests locally: `python -m pytest tests/ -v`

4. **Update documentation** if needed:
   - Update README.md for user-facing changes
   - Update docs/grammar-spec.md for DSL grammar changes
   - Keep docstrings current

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions and variables
- Keep functions focused and well-documented
- Add docstrings to public APIs

### Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_mvp_parser.py -v

# Run with coverage
python -m pytest tests/ --cov=llm_flow_dsl
```

## Submitting Changes

### Pull Request Process

1. **Push** your branch to your fork:
   ```bash
   git push origin your-branch-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to any related issues (e.g., "Fixes #123")
   - Screenshots or examples if relevant

3. **Respond to feedback** from reviewers
   - All feedback is constructive and intended to improve the project
   - Request changes or clarification if feedback is unclear

4. **Ensure CI passes**:
   - All tests must pass
   - No new linting errors
   - Code coverage should not decrease

## Reporting Bugs

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant error messages or logs

## Suggesting Enhancements

When suggesting features:

- Explain the use case and why it would be valuable
- Provide examples of how it would be used
- Consider the impact on existing functionality

## Questions?

- Check existing issues and discussions
- Ask in GitHub Discussions
- Refer to docs/grammar-spec.md for DSL details

## Recognition

Contributors will be credited in CONTRIBUTORS.md and acknowledged in release notes. Thank you for making llm-flow-dsl better!
