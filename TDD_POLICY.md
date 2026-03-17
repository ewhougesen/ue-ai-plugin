# TDD Policy (MANDATORY)

**This project follows TEST DRIVEN DEVELOPMENT (TDD) as a mandatory standard.**

## The Iron Rule

```
NO CODE WITHOUT TESTS FIRST.
```

If you haven't written a failing test, you cannot write implementation code.

---

## TDD Workflow (Strictly Enforced)

### 1. RED - Write a Failing Test
- Write a test that describes the behavior you want
- Run the test - it MUST fail
- If it passes, you're not testing anything new

### 2. GREEN - Make It Pass
- Write the MINIMUM code to make the test pass
- Don't worry about perfection yet
- Just make the test pass

### 3. REFACTOR - Clean Up
- Improve the code while keeping tests green
- Remove duplication
- Enhance readability

---

## Project Structure

```
backend/
├── app/                    # Implementation code
│   ├── services/
│   ├── grpc_server/
│   └── models/
├── tests/                  # TESTS (mirror app structure)
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── conftest.py        # Pytest configuration
│   └── fixtures/          # Test fixtures
└── pytest.ini             # Pytest settings
```

---

## Rules

1. **Never commit without tests** - All commits must include passing tests
2. **Test first, always** - No exceptions, no "I'll add tests later"
3. **Coverage threshold** - Minimum 80% code coverage
4. **No skipping tests** - Broken tests must be fixed before proceeding
5. **CI/CD gate** - Tests must pass before merging

---

## Test Categories

| Type | Purpose | Speed |
|------|---------|-------|
| **Unit** | Test individual functions/classes | Fast |
| **Integration** | Test service interactions | Medium |
| **E2E** | Test complete workflows | Slow |

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_claude_service.py

# Run fast tests only
pytest -m "not slow"
```

---

## Examples

### ❌ WRONG (Code first, tests later)
```python
# app/services/calculator.py
def add(a, b):
    return a + b

# Later... write tests (BAD!)
```

### ✅ RIGHT (Test first)
```python
# tests/unit/test_calculator.py
def test_add_two_numbers():
    result = add(2, 3)
    assert result == 5

# Run: FAILS (function doesn't exist yet)

# NOW write code:
# app/services/calculator.py
def add(a, b):
    return 2 + 3  # Minimum to pass

# Run: PASSES

# Refactor:
def add(a, b):
    return a + b  # Clean implementation
```

---

## Pre-Commit Checklist

Before committing, run:

```bash
pytest --cov=app --cov-fail-under=80
```

If this fails, **DO NOT COMMIT**.

---

## Adding New Features

1. Write test describing the feature
2. Run test (fails)
3. Implement feature
4. Run test (passes)
5. Refactor
6. Commit

---

**Remember: Tests are not optional. Tests are not "later". Tests are FIRST.**

---

*This policy is enforced for all development on this project.*
