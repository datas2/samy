# Python Best Practices

This document collects core Python best practices and idioms used by Samy’s
Python skills: refactor, review, tests, docstring, and FastAPI. It is designed
to be readable by both humans and Samy’s RAG/LLM pipeline.

---
## 1. General Style & Readability
### 1.1 Naming Conventions

- Use `snake_case` for functions and variables.
- Use `PascalCase` for classes.
- Use `UPPER_SNAKE_CASE` for constants.

```python
def calculate_total(price: float, quantity: int) -> float:
    total_price = price * quantity
    return total_price


class OrderProcessor:
    MAX_RETRIES = 3

    def process(self, order_id: str) -> None:
        ...
```

Guidelines:
- Names should be descriptive and reflect intent (`total_price`, not `tp`).
- Avoid abbreviations unless widely known (`db`, `id`, `url`).

## 1.2 Functions & Cohesion
- Prefer small, focused functions that do one thing well.
- Avoid functions with too many responsibilities.
- Use explicit parameters instead of hidden globals.

```python
def compute_discount(amount: float, customer_type: str) -> float:
    """Compute discount based on customer type."""
    if customer_type == "vip":
        return amount * 0.2
    if customer_type == "regular":
        return amount * 0.1
    return 0.0
```

Good practices:
- Keep functions short and easy to read.
- Return early instead of deeply nested if chains when appropriate.

## 1.3 Control Flow & Readability
- Prefer clear control flow to clever one-liners.
- Use for loops instead of complex comprehensions when logic is non-trivial.

```python
def filter_active_users(users: list[dict]) -> list[dict]:
    active_users = []
    for user in users:
        if user.get("is_active"):
            active_users.append(user)
    return active_users
```

Avoid overly complex expressions:

```python
# Harder to read
active_users = [u for u in users if u.get("is_active") and u.get("age", 0) > 18]

# Better: readable condition
def is_active_adult(user: dict) -> bool:
    return bool(user.get("is_active")) and user.get("age", 0) > 18

active_users = [u for u in users if is_active_adult(u)]
```

---
# 2. Error Handling & Logging
## 2.1 Specific Exceptions
- Catch specific exceptions rather than bare except.
- Avoid swallowing exceptions silently.

```python
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config(path: str) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
        return json.loads(text)
    except FileNotFoundError:
        logger.error("Config file not found: %s", path)
        raise
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in config file %s: %s", path, exc)
        raise
```

Guidelines:
- Always log meaningful messages when catching and re-raising exceptions.
- Only use bare `except` when you truly want to catch all exceptions, and log them.

## 2.2 Graceful Degradation
- Provide fallbacks for non-critical features.
- Keep the main flow running when possible.

```python
def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except ValueError:
        return default
```

Use this pattern for non-critical parsing/formatting, but not for core business logic where errors must be surfaced.

---
# 3. Types & Interfaces
## 3.1 Type Hints
- Use type hints for function parameters and return types.
- Prefer modern annotations (`list[int]`, `dict[str, Any]`) on Python 3.9+.

```python
from typing import Any


def add(a: int, b: int) -> int:
    return a + b


def get_config_value(config: dict[str, Any], key: str, default: Any = None) -> Any:
    return config.get(key, default)
```

Benefits:
- Improve readability and maintainability.
- Help tools (linters, type checkers) catch errors earlier.

## 3.2 Data Structures
- Use `dataclasses` for simple data containers.
- Prefer explicit structures over ad-hoc dictionaries when possible.

```python
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    is_active: bool = True
```

---
# 4. Testing Best Practices (pytest)
Samy’s Python tests skill (`PythonTestsSkill`) should prefer idiomatic pytest patterns.

## 4.1 Arrange–Act–Assert Structure
- Structure tests clearly into Arrange, Act, Assert.
- Use comments or blank lines to separate phases.

```python
import pytest

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (-1, 1, 0),
    ],
)
def test_add(a: int, b: int, expected: int) -> None:
    
    # Arrange

    
    # Act
    result = add(a, b)

    
    # Assert
    assert result == expected
```

## 4.2 Fixtures for Setup
- Use fixtures for shared setup.
- Keep tests focused on behavior, not on wiring.

```python
import pytest


@pytest.fixture
def temp_user() -> User:
    return User(id=1, name="Alice")


def test_user_is_active_by_default(temp_user: User) -> None:
    
    # Act
    is_active = temp_user.is_active

    
    # Assert
    assert is_active is True
```

## 4.3 Parametrized Tests
- Use `@pytest.mark.parametrize` to cover multiple cases.
- Keep test names descriptive.

```python
@pytest.mark.parametrize(
    "value,default,expected",
    [
        ("10", 0, 10),
        ("abc", 0, 0),
        ("", 5, 5),
    ],
)
def test_parse_int(value: str, default: int, expected: int) -> None:
    
    # Act
    result = parse_int(value, default)

    
    # Assert
    assert result == expected
```

---
# 5. Docstring Conventions (Google Style)
Samy’s docstring skill (`PythonDocstringSkill`) should follow a clear convention. Google style is a good default.

## 5.1 Function Docstrings
```python
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The sum of `a` and `b`.
    """
    return a + b
```

Guidelines:
- Start with a one-line summary.
- Use `Args:` section for parameters.
- Use `Returns:` section for return type and meaning.
- Use `Raises:` when the function may raise exceptions intentionally.

```python
def divide(a: float, b: float) -> float:
    """Divide `a` by `b`.

    Args:
        a: Numerator.
        b: Denominator.

    Returns:
        The result of a / b.

    Raises:
        ZeroDivisionError: If `b` is zero.
    """
    return a / b
```

---
# 6. FastAPI Best Practices
Samy’s FastAPI skill (`PythonFastAPISkill`) should generate endpoints that are:
- Clear
- Typed
- Structured

## 6.1 Basic Endpoint Pattern
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class AddRequest(BaseModel):
    a: int
    b: int


class AddResponse(BaseModel):
    result: int


@app.post("/add", response_model=AddResponse)
def add_numbers(request: AddRequest) -> AddResponse:
    """Add two numbers provided in the request body."""
    result = request.a + request.b
    return AddResponse(result=result)
```

Best practices:
- Use Pydantic models for request and response bodies.
- Add docstrings to endpoints describing behavior.
- Use explicit `response_model` for structured responses.

## 6.2 Dependency Injection & Error Handling
```python
from fastapi import Depends, HTTPException


def get_db():
    # example placeholder; in real code, return a DB session
    return {}


@app.get("/items/{item_id}")
def get_item(item_id: int, db = Depends(get_db)):
    """Retrieve an item by its ID."""
    item = db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

Guidelines:
- Use `Depends` for shared resources (DB, config, services).
- Use `HTTPException` for clear, consistent error responses.

---
# 7. Guidelines for Code Review & Refactoring
When Samy’s refactor and review skills process Python code, they should:
- Preserve Behavior
    - Do not change the logical behavior of the code unless explicitly requested.
    - Focus first on readability and maintainability.
- Improve Readability
    - Use clear names and consistent style.
    - Reduce nesting where possible.
    - Split long functions into smaller ones when it improves clarity.
- Encourage Type Hints
    - Add type hints for public functions.
    - Prefer explicit return types.
- Remove Dead Code
    - Delete unused variables and unreachable branches.
    - Avoid commented-out blocks of obsolete code.
- Enhance Error Handling & Logging
    - Catch specific exceptions and log meaningful messages.
    - Avoid silent failures.
- Keep it code simple
    - Prefer writing less code over large functions.
    - Evaluate when code can be removed without compromising business logic.

---
# 8. References & Standards
Prefer solutions aligned with the following standards:
- PEP 8 – Style Guide for Python Code
    https://peps.python.org/pep-0008/
- PEP 20 – The Zen of Python
    https://peps.python.org/pep-0020/
- PEP 484 – Type Hints
    https://peps.python.org/pep-0484/
- Python Documentation
    https://docs.python.org/3/

Samy’s Python skills should treat these as guiding references when generating, refactoring, or reviewing code.