# Testing Guide

This directory contains tests for the Flask Note App. The tests are organized into three categories:

1. Unit Tests (`tests/unit/`)

   - Test individual components in isolation
   - Focus on models and utility functions
   - Fast execution

2. Integration Tests (`tests/integration/`)

   - Test interactions between components
   - Focus on authentication and database operations
   - Medium execution speed

3. Functional Tests (`tests/functional/`)
   - Test complete features from user perspective
   - Focus on note operations and sharing
   - Slower execution

## Running Tests

1. Install test dependencies:

```bash
pip install -r requirements-test.txt
```

2. Run all tests:

```bash
pytest
```

3. Run specific test categories:

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Functional tests only
pytest tests/functional/
```

4. Run with coverage report:

```bash
pytest --cov=website
```

## Test Organization

- `conftest.py`: Contains shared fixtures and configuration
- `unit/`: Unit tests for models and utilities
- `integration/`: Tests for component interactions
- `functional/`: End-to-end feature tests
- `fixtures/`: Test data and mock objects

## Writing New Tests

1. Choose the appropriate test category
2. Follow the existing test patterns
3. Use fixtures from `conftest.py` when possible
4. Add descriptive docstrings
5. Keep tests focused and independent
