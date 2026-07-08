# 1. Goals of Tests
- Verify behavior, not implementation details.
- Provide confidence when refactoring.
- Catch regressions quickly.
- Document expected usage (examples) of functions and modules.

Guideline:
- Tests should focus on what the code should do, not how it does it.

---
# 2. Structure and Style (pytest)
## 2.1 Arrange – Act – Assert
- Use the AAA pattern in all tests.
- Separate phases with comments and blank lines for clarity.

```python
import pytest

def test_add():
    
    # Arrange
    a = 1
    b = 2

    
    # Act
    result = add(a, b)

    
    # Assert
    assert result == 3
```
Samy’s generated tests should always follow AAA, with explicit comments.

## 2.2 Fixtures
- Use fixtures for shared setup (DB, configuration, temporary files).
- Keep tests focused on behavior, not wiring.

```python
import pytest

@pytest.fixture
def sample_user():
    return User(id=1, name="Alice")

def test_user_is_active_by_default(sample_user):
    
    # Act
    is_active = sample_user.is_active

    
    # Assert
    assert is_active is True
```

Guidelines:
- Fixtures should be small and composable.
- Avoid overly complex fixture trees that hide behavior.

## 2.3 Parametrized Tests
- Use `@pytest.mark.parametrize` to cover multiple inputs/outputs.
- Provide meaningful `ids` for each case when useful.

```python
@pytest.mark.parametrize(
    "value,default,expected",
    [
        pytest.param("10", 0, 10, id="valid-int"),
        pytest.param("abc", 0, 0, id="invalid-int-returns-default"),
        pytest.param("", 5, 5, id="empty-string-returns-default"),
    ],
)
def test_parse_int(value, default, expected):
    
    # Act
    result = parse_int(value, default)

    
    # Assert
    assert result == expected
```

---
# 3. Scope and Granularity
## 3.1 Unit Tests
- Test isolated functions and classes.
- Avoid hitting external systems (DB, HTTP) directly in unit tests.

Guidelines:
- Focus on a single function/method per test.
- Use mocks or fakes for external dependencies.

## 3.2 Integration Tests
- Test interactions between modules, DB, HTTP clients, etc.
- Use realistic configuration and data.

Guidelines:
- Separate integration tests from unit tests (e.g., different directories).
- Accept that integration tests may be slower, but still deterministic.

---
# 4. Behavior vs Implementation
- Test **public interfaces** and behavior.
- Avoid testing private/internal helpers unless necessary.
- Do not assert on internal implementation details (e.g., exact SQL query string) unless that is part of the contract.

Example:

```python
def test_repository_saves_event(db_session):
    
    # Arrange
    repo = TelemetryRepository(db=db_session)

    
    # Act
    repo.save_event("test_event", {"foo": "bar"})

    
    # Assert
    events = repo.list_events(event_type="test_event")
    assert len(events) == 1
    assert events[0].payload == {"foo": "bar"}
```

Here we test the behavior of `save_event` and `list_events`, not how the ORM is configured internally.

---
# 5. Error Handling and Edge Cases
- Tests should cover:
    - Normal (“happy path”) scenarios.
    - Edge cases (empty inputs, large values, nulls).
    - Error cases (invalid input, exceptions, resource failures).

Guidelines:
- Use parametrized tests to cover multiple edge cases.
- Test that functions raise the correct exceptions and messages.

```python
def test_divide_raises_zero_division():
    
    # Act / Assert
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

---
# 6. Isolation and Determinism
- Tests must be deterministic: same input → same output, every run.
- Avoid reliance on network, time, randomness without control.

Guidelines:
- Mock or freeze time when necessary.
- Seed random generators or avoid randomness in tests.
- Clean up resources (files, DB records) after tests, via fixtures or teardown.

```python
from freezegun import freeze_time

@freeze_time("2024-01-01")
def test_timestamp_generation():
    
    # Act
    ts = generate_timestamp()

    
    # Assert
    assert ts == "2024-01-01T00:00:00Z"
```

---
# 7. Naming and Organization
## 7.1 Test Names
- Use descriptive names expressing behavior: `test_add_returns_sum`, `test_repo_saves_event`.
- Avoid generic names like `test_function1`.

## 7.2 Structure
- Organize tests by module or feature: `tests/unit/backend/skills/test_python.py`, `tests/integration/backend/skills/test_skills_sql.py`.
- Keep test files small and focused.

Guidelines:
- Group related tests in the same file.
- Use markers (`@pytest.mark.integration`, `@pytest.mark.asyncio`) to distinguish types of tests.

---
# 8. Use of Tools
## 8.1 Coverage
- Aim for high coverage (e.g., ≥ 90%), but prioritize meaningful tests over coverage numbers.
- Use `coverage.py` or `pytest --cov` to measure test coverage.

Guidelines:
- Ensure critical paths (error handling, branching logic) are covered.
- Don’t write contrived tests just to raise coverage.

# 8.2 Property-Based Testing (Optional)
- For pure functions, consider Hypothesis or similar tools.
- Test properties like “commutativity” (`add(a, b) == add(b, a)`) or “idempotence”.

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    
    # Act
    result1 = add(a, b)
    result2 = add(b, a)

    
    # Assert
    assert result1 == result2
```

---
# 9. Guidelines for Samy’s Test Generation (PythonTestsSkill)
When Samy generates tests for Python code, it should:

- Use **pytest** as the default framework.
- Follow the **Arrange–Act–Assert** pattern with comments and blank lines.
- Include **happy path, edge cases, and error cases** when possible.
- Prefer **type hints** in test code where helpful.
- Use **fixtures** for shared setup rather than duplicating code.
- Use **parametrized tests** to avoid repetitive test functions.
- Avoid hitting external systems directly; prefer mocks/fakes in unit tests.
- Name tests clearly based on behavior (`test_<function>_<scenario>`).

---
# 10. External References & Further Reading

These resources provide deeper background and examples that align with the
testing guidelines used by Samy’s Python skills.

## 10.1 pytest

- **pytest Official Documentation**  
  https://docs.pytest.org/en/stable/  
  Comprehensive guide to pytest features: fixtures, parametrization, markers,
  plugins, and test discovery. Samy’s generated tests should be compatible
  with these patterns.

- **“Effective Python Testing With pytest” (Real Python)**  
  https://realpython.com/pytest-python-testing/  
  Practical introduction to pytest with idiomatic examples, including
  fixtures, parametrized tests, and test organization.

## 10.2 Coverage & Quality

- **coverage.py Documentation**  
  https://coverage.readthedocs.io/  
  Explains how to measure code coverage, configure reports, and integrate
  coverage with pytest (`pytest --cov`).

- **“Testing and Continuous Integration” – Python Packaging User Guide**  
  https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#testing  
  Overview of testing in the context of packaging and CI, useful for
  integrating tests into pipelines.

## 10.3 Property-Based Testing

- **Hypothesis – Property-Based Testing for Python**  
  https://hypothesis.readthedocs.io/  
  Documentation for Hypothesis, a library that generates test cases from
  specifications. Useful for testing functions with complex input spaces.

## 10.4 General Testing Practices

- **“Unit Testing” – Python Docs (unittest)**  
  https://docs.python.org/3/library/unittest.html  
  Standard library testing framework. Samy prefers pytest, but unittest
  concepts are still relevant and often encountered in existing codebases.

- **Martin Fowler – “Test Pyramid”**  
  https://martinfowler.com/bliki/TestPyramid.html  
  Conceptual guide to balancing unit, integration, and end-to-end tests,
  aligning with Samy’s testing strategy (most tests should be unit-level).

---

When Samy’s test-related skills generate or review tests, they should favor
patterns and practices consistent with these references, while adapting to
the specific project context (frameworks, CI setup, codebase size).
