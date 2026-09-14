# Python Interview Handbook for AI Engineers and Architects

This handbook is deliberately limited to the Python-focused interview round. It does not cover RAG, LLM frameworks, vector databases, prompt engineering, or AI system design.

The goal is not to memorize every Python feature. The goal is to be able to:

1. Explain the important concepts clearly.
2. Predict what a short Python program will do.
3. Write clean, correct code without relying heavily on an IDE.
4. Discuss trade-offs expected from a senior engineer or architect.

All examples assume Python 3.10 or later unless stated otherwise.

---

## Index

### Start here

1. [What is actually required?](#what-is-actually-required)
2. [How to use this handbook](#how-to-use-this-handbook)
3. [A practical preparation sequence](#a-practical-preparation-sequence)

### Must Know

1. [Core data model: objects, mutability, identity, and copying](#1-core-data-model-objects-mutability-identity-and-copying)
2. [Collections, comprehensions, and essential built-ins](#2-collections-comprehensions-and-essential-built-ins)
3. [Functions, arguments, scope, closures, and imports](#3-functions-arguments-scope-closures-and-imports)
4. [Object-oriented Python and the Python data model](#4-object-oriented-python-and-the-python-data-model)
5. [Iterables, iterators, and generators](#5-iterables-iterators-and-generators)
6. [Decorators](#6-decorators)
7. [Exceptions and context managers](#7-exceptions-and-context-managers)
8. [Type hints and interface design](#8-type-hints-and-interface-design)
9. [Concurrency: threads, processes, and asyncio](#9-concurrency-threads-processes-and-asyncio)
10. [Testing, mocking, and debugging](#10-testing-mocking-and-debugging)
11. [Coding problems and complexity](#11-coding-problems-and-complexity)

### Good To Know

12. [Files, JSON, serialization, and parsing](#12-files-json-serialization-and-parsing)
13. [Memory management and performance](#13-memory-management-and-performance)
14. [Environments and packaging](#14-environments-and-packaging)
15. [Useful standard-library tools](#15-useful-standard-library-tools)

### Practice Resources

1. [YouTube learning links](#youtube-learning-links)
2. [Python coding-practice links](#python-coding-practice-links)
3. [Final mock-round checklist](#final-mock-round-checklist)

---

## What is actually required?

No, every item in a large "Python mastery" roadmap is not required for one Python interview round.

### Must Know

These topics have the highest probability of appearing in a Python round and are also useful in day-to-day AI backend work:

| Priority | Area | Required depth |
|---|---|---|
| 1 | Core data model and collections | Explain behavior and solve small code-output questions |
| 2 | Functions, scope, arguments, and imports | Write functions correctly, identify common traps, and explain module execution |
| 3 | OOP and Python data model | Design a small class and explain inheritance/composition |
| 4 | Iterators and generators | Build a generator and explain lazy evaluation |
| 5 | Decorators | Read and write one practical decorator |
| 6 | Exceptions and context managers | Handle errors and cleanup resources correctly |
| 7 | Typing | Type normal application code and explain that hints are not runtime enforcement |
| 8 | Concurrency and asyncio | Select the right model and write basic async code |
| 9 | Testing and debugging | Test behavior, dependencies, and failures |
| 10 | Coding and complexity | Solve easy-to-medium problems in readable Python |

### Good To Know

These topics help distinguish a senior candidate, but they should come after the MUST topics:

| Area | Sensible interview depth |
|---|---|
| Files and serialization | Read/write JSON safely; know why untrusted pickle is dangerous |
| Memory and performance | Understand references, garbage collection basics, profiling, and Big-O |
| Packaging and environments | Explain virtual environments, dependency metadata, and reproducible installs |
| Advanced standard library | Recognize `itertools`, `functools`, `collections`, and `heapq` use cases |

### Usually not worth prioritizing for this round

Study these only when the job description specifically asks for them:

- CPython bytecode and interpreter implementation details
- Descriptor internals and metaclasses
- `__slots__` edge cases
- Weak references and manual garbage-collector tuning
- C extensions, the buffer protocol, and `memoryview`
- Experimental free-threaded/no-GIL implementation details
- Custom event-loop implementation
- Advanced generic variance and type-checker internals

---

## How to use this handbook

For each section, use this four-step loop:

1. **Read** the explanation and run the example.
2. **Predict** the output before running code-output examples.
3. **Implement** the exercises without looking at the example.
4. **Explain aloud** why your solution works and state its time and space complexity.

A concept is interview-ready when you can explain it in two minutes, write a small example from memory, and answer one follow-up question about trade-offs.

Avoid passively watching several hours of video. A useful ratio is 30% reading/video and 70% writing, testing, and explaining code.

## A practical preparation sequence

Use this order if time is limited:

1. Sections 1-3: core language fluency
2. Sections 4-7: Python-specific design features
3. Sections 8-10: production Python
4. Section 11: timed coding throughout preparation
5. Sections 12-15: second-pass knowledge

For every 60-minute study session:

- 15 minutes: learn one concept
- 30 minutes: code two exercises
- 10 minutes: explain the solution aloud
- 5 minutes: write down mistakes and review them the next day

---

## Must Know

### 1. Core data model: objects, mutability, identity, and copying

#### Mental model

Python variables are names bound to objects. Assignment does not normally copy an object; it creates another reference to it.

```python
first = [1, 2]
second = first
second.append(3)

print(first)          # [1, 2, 3]
print(first is second)  # True
```

`first` and `second` refer to the same list. The list changed; neither variable was "copied."

#### Mutable and immutable objects

Common immutable types:

- `int`, `float`, `bool`
- `str`, `bytes`
- `tuple` (although it may contain a mutable object)
- `frozenset`

Common mutable types:

- `list`
- `dict`
- `set`
- most user-defined class instances

```python
name = "Ada"
original_id = id(name)
name += " Lovelace"

print(id(name) == original_id)  # Usually False: a new string was created
```

#### `==` versus `is`

- `==` asks whether two values are equal.
- `is` asks whether both names refer to the exact same object.
- Use `is None` and `is not None` for `None` checks.

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True
print(a is b)  # False
```

Do not use object interning behavior as business logic. Small integers or some strings may share identities as an implementation optimization.

#### Shallow versus deep copy

A shallow copy creates a new outer container but keeps references to nested objects. A deep copy recursively copies nested objects.

```python
from copy import copy, deepcopy

source = {"scores": [10, 20]}
shallow = copy(source)
deep = deepcopy(source)

source["scores"].append(30)

print(shallow)  # {'scores': [10, 20, 30]}
print(deep)     # {'scores': [10, 20]}
```

#### Function arguments use object sharing

Python passes object references by assignment. A function can mutate an object it receives, but rebinding the local parameter does not rebind the caller's variable.

```python
def change(values: list[int]) -> None:
    values.append(4)       # Mutates the caller's list
    values = [99]          # Rebinds only the local name


numbers = [1, 2, 3]
change(numbers)
print(numbers)  # [1, 2, 3, 4]
```

#### Classic trap: mutable default arguments

Default argument objects are created once when the function is defined, not once per call.

```python
def add_event(event: str, events: list[str] | None = None) -> list[str]:
    if events is None:
        events = []
    events.append(event)
    return events
```

#### Likely interview questions

- What is the difference between `is` and `==`?
- Why is a mutable default argument dangerous?
- What changes when a list is passed to a function?
- What is the difference between a shallow and deep copy?
- Can a tuple contain a list? Is that tuple hashable?

#### Exercises

1. Predict the output, then run it:

   ```python
   grid = [[0] * 3] * 3
   grid[0][0] = 1
   print(grid)
   ```

   Then create the grid correctly so that each row is independent.

2. Write `safe_add_tag(tag, tags=None)` that never shares a default list across calls.
3. Write a function that returns a modified copy of a nested configuration without changing the input.
4. Create two distinct `User` objects that compare equal by value. This prepares you for `__eq__` in Section 4.

---

### 2. Collections, comprehensions, and essential built-ins

#### Choosing the correct collection

| Type | Ordered | Mutable | Duplicates | Typical use |
|---|---|---|---|---|
| `list` | Yes | Yes | Yes | Sequence of items |
| `tuple` | Yes | No | Yes | Fixed record or immutable sequence |
| `dict` | Insertion ordered | Yes | Keys unique | Key-value lookup |
| `set` | Do not rely on display order | Yes | No | Membership and de-duplication |
| `frozenset` | Do not rely on display order | No | No | Immutable set or dictionary key |

Average membership lookup is O(1) for a `set` or `dict`, but O(n) for a `list` or `tuple`.

```python
allowed_ids = {101, 205, 410}

if 205 in allowed_ids:
    print("allowed")
```

#### Comprehensions

Use comprehensions for short transformations and filtering. Prefer a normal loop when the logic has several branches or side effects.

```python
scores = {"a": 82, "b": 49, "c": 91}
passed = {name: score for name, score in scores.items() if score >= 50}
```

#### Unpacking

```python
first, *middle, last = [10, 20, 30, 40]
coordinates = (12, 8)
x, y = coordinates
```

Dictionary merging in modern Python:

```python
defaults = {"timeout": 10, "retries": 2}
overrides = {"timeout": 30}
config = defaults | overrides
```

#### Essential built-ins

Know how and when to use:

- `enumerate(items)` for index-value pairs
- `zip(a, b)` for parallel iteration
- `sorted(items, key=..., reverse=...)` for a new sorted list
- `min`, `max`, and `sum`
- `any` and `all`
- `map` and `filter` (and when a comprehension is clearer)

```python
employees = [
    {"name": "Mina", "level": 3},
    {"name": "Raj", "level": 1},
]

by_level = sorted(employees, key=lambda item: item["level"])
```

#### Common collection tools

```python
from collections import Counter, defaultdict, deque

counts = Counter("mississippi")

groups: defaultdict[str, list[int]] = defaultdict(list)
groups["odd"].append(3)

queue = deque(["job-1", "job-2"])
next_job = queue.popleft()
```

Use `deque.popleft()` for an efficient queue. Removing index 0 from a list is O(n).

#### Likely interview questions

- When would you choose a tuple over a list?
- Why is a set faster for membership checks?
- Are dictionaries ordered?
- How do you remove duplicates while preserving order?
- What is the difference between `list.sort()` and `sorted()`?
- When is a comprehension too complex?

#### Exercises

1. Remove duplicates from a list while preserving first-seen order.
2. Count words case-insensitively and return the three most common words.
3. Group a list of employees by department with `defaultdict`.
4. Join two lists, `names` and `scores`, into a dictionary using `zip`.
5. Sort API records by descending priority, then ascending creation time.
6. Implement a queue twice: once with a list and once with `deque`; explain the complexity difference.

---

### 3. Functions, arguments, scope, closures, and imports

#### Functions are objects

Functions can be assigned to names, stored in collections, passed to other functions, and returned from functions.

```python
from collections.abc import Callable


def apply(value: int, operation: Callable[[int], int]) -> int:
    return operation(value)


def double(value: int) -> int:
    return value * 2


print(apply(5, double))  # 10
```

#### Positional, keyword, and constrained arguments

```python
def request(
    url: str,
    /,
    method: str = "GET",
    *,
    timeout: float = 10.0,
) -> None:
    print(url, method, timeout)
```

- Parameters before `/` are positional-only.
- Parameters after `*` are keyword-only.
- Keyword-only parameters make important call-site options clearer.

#### `*args` and `**kwargs`

```python
def log_event(event: str, *tags: str, **metadata: object) -> None:
    print(event, tags, metadata)


log_event("login", "security", "user", user_id=42, success=True)
```

Use them when forwarding flexible arguments or building a genuinely flexible API. Do not use them just to avoid designing a clear signature.

#### LEGB scope

Python resolves a name in this order:

1. Local
2. Enclosing
3. Global
4. Built-in

`global` rebinds a module-level name. `nonlocal` rebinds a name in the nearest enclosing function scope.

```python
def make_counter() -> Callable[[], int]:
    count = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment
```

The returned function is a closure because it retains access to `count` after `make_counter` has returned.

#### Late binding in closures

Closures look up captured variables when called, which can surprise people in loops.

```python
functions = [lambda value=i: value for i in range(3)]
print([function() for function in functions])  # [0, 1, 2]
```

The default parameter captures the current value of `i` during each iteration.

#### Modules, imports, and the main guard

A module is normally one `.py` file. Importing it executes its top-level code the first time in a process and caches the module object in `sys.modules`; later imports normally reuse that object.

Keep expensive work and surprising side effects out of module-level code. Circular imports often indicate that responsibilities should move to a lower-level module or that a dependency boundary needs redesigning.

```python
def main() -> None:
    print("run application")


if __name__ == "__main__":
    main()
```

The main guard prevents `main()` from running merely because another module imports the file. It is also important when starting child processes on platforms that import the main module in the new process.

#### Likely interview questions

- Explain LEGB.
- What is a closure and where is it useful?
- What is the difference between `global` and `nonlocal`?
- Explain `*args` and `**kwargs`.
- What are positional-only and keyword-only arguments?
- Are lambdas different from normal functions?
- What happens the first time a module is imported?
- What does `if __name__ == "__main__"` prevent?
- Why do circular imports happen, and how would you redesign them?

#### Exercises

1. Write `make_multiplier(factor)` that returns a function multiplying by `factor`.
2. Fix a loop that creates three callbacks but accidentally returns the final loop value from all three.
3. Write a function whose `timeout` and `retries` parameters must be supplied by keyword.
4. Write `compose(f, g)` so `compose(f, g)(x)` returns `f(g(x))`.
5. Explain why excessive `global` state makes testing and concurrency harder.
6. Split a small script into two modules while keeping execution behind a main guard.

---

### 4. Object-oriented Python and the Python data model

#### Classes and instances

A class defines behavior and data shared by a kind of object. Each instance has its own state.

```python
class RateLimit:
    default_limit = 100  # Class variable

    def __init__(self, user_id: str, limit: int | None = None) -> None:
        self.user_id = user_id
        self.limit = limit if limit is not None else self.default_limit

    def allows(self, used: int) -> bool:
        return used < self.limit
```

Know the difference between class variables and instance variables. A mutable class variable is shared across instances and is often a bug.

#### Instance, class, and static methods

- Instance method: receives `self`; works with instance state.
- Class method: receives `cls`; often an alternative constructor.
- Static method: receives neither; a utility logically owned by the class.

```python
from dataclasses import dataclass


@dataclass
class Endpoint:
    host: str
    port: int

    @classmethod
    def from_address(cls, address: str) -> "Endpoint":
        host, port = address.rsplit(":", 1)
        return cls(host=host, port=int(port))
```

#### Inheritance, MRO, and `super()`

The method resolution order (MRO) defines where Python searches for a method in an inheritance hierarchy. `super()` follows that order; it does not simply mean "call my parent."

```python
class BaseClient:
    def request(self) -> str:
        return "base"


class LoggedClient(BaseClient):
    def request(self) -> str:
        result = super().request()
        return f"logged: {result}"
```

Prefer composition when an object *has a* dependency. Use inheritance when the subtype genuinely *is a* substitutable version of the base type.

#### Dunder methods

Special methods let custom objects participate in normal Python operations.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    prompt: int
    completion: int

    @property
    def total(self) -> int:
        return self.prompt + self.completion


usage = TokenUsage(prompt=120, completion=30)
print(usage.total)  # 150
```

Frequently discussed methods include `__init__`, `__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, and `__iter__`.

Use a dunder method only when the operation has its conventional meaning. For example, `__len__` should represent the number of items in an object, not an unrelated numeric total.

#### Dataclasses and properties

Use a dataclass for a data-focused class to generate methods such as `__init__`, `__repr__`, and `__eq__`.

Use a property when callers should access something like an attribute but logic is needed to calculate or validate it.

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32
```

#### Likely interview questions

- Class variable versus instance variable?
- `@classmethod` versus `@staticmethod`?
- What does `super()` do?
- Composition versus inheritance?
- `__str__` versus `__repr__`?
- What does `@dataclass` generate?
- What makes an object hashable?

#### Exercises

1. Build a `Task` dataclass with `id`, `priority`, and `created_at`, then sort tasks.
2. Add value-based equality and a useful representation to a small class.
3. Implement a `Client.from_url()` alternative constructor.
4. Refactor an inheritance design into composition and explain why it is easier to test.
5. Create an immutable, hashable `Coordinate` dataclass that can be a dictionary key.

---

### 5. Iterables, iterators, and generators

#### Iterable versus iterator

An iterable can produce an iterator. An iterator produces one value at a time and remembers its position.

- Iterable protocol: `__iter__()` returns an iterator.
- Iterator protocol: `__iter__()` returns itself and `__next__()` returns the next item or raises `StopIteration`.

```python
values = [10, 20, 30]
iterator = iter(values)

print(next(iterator))  # 10
print(next(iterator))  # 20
```

A list is iterable but not itself an iterator. A generator object is both.

#### Generators and lazy evaluation

A function containing `yield` creates a generator. Its body pauses at each `yield` and resumes on the next request.

```python
from collections.abc import Iterator


def read_batches(items: list[int], size: int) -> Iterator[list[int]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


for batch in read_batches([1, 2, 3, 4, 5], size=2):
    print(batch)
```

Generators are useful for large files, streams, paginated results, and pipelines because they avoid storing the entire result at once.

#### Generator expressions

```python
total = sum(number * number for number in range(1_000_000))
```

The expression supplies values to `sum` lazily instead of first creating a million-element list.

#### One-pass behavior

An iterator is normally consumed once.

```python
generator = (value * 2 for value in range(3))
print(list(generator))  # [0, 2, 4]
print(list(generator))  # []
```

#### `yield from`

`yield from iterable` delegates iteration to another iterable.

```python
def flatten(groups: list[list[int]]):
    for group in groups:
        yield from group
```

#### Likely interview questions

- Iterable versus iterator?
- What does `yield` do?
- Generator versus list: what are the trade-offs?
- Why can a generator be exhausted?
- What happens when `next()` has no more values?
- When would lazy evaluation be a bad choice?

#### Exercises

1. Write `countdown(start)` as a generator.
2. Write a generator that reads a large text file one non-empty line at a time.
3. Create a custom `RangeLike` iterator without using `range` internally.
4. Implement lazy pagination that requests the next page only when needed.
5. Compare the approximate memory used by a list comprehension and generator expression for one million integers.

---

### 6. Decorators

#### Mental model

A decorator takes a callable and returns a callable. The `@decorator` syntax is convenient assignment syntax.

```python
@trace
def calculate() -> int:
    return 42
```

is conceptually equivalent to:

```python
def calculate() -> int:
    return 42


calculate = trace(calculate)
```

#### A practical decorator

```python
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timed(function: Callable[P, R]) -> Callable[P, R]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        started = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            elapsed = perf_counter() - started
            print(f"{function.__name__}: {elapsed:.4f}s")

    return wrapper
```

`functools.wraps` preserves metadata such as the original function's name and documentation. It also helps introspection tools follow the wrapped function.

#### Decorator with arguments

```python
from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(attempts: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: Exception | None = None

            for attempt in range(attempts):
                try:
                    return function(*args, **kwargs)
                except Exception as error:
                    last_error = error
                    if attempt < attempts - 1:
                        sleep(0.1)

            assert last_error is not None
            raise last_error

        return wrapper

    return decorate
```

In production, retry only errors that are actually transient, add backoff/jitter, and avoid retrying non-idempotent operations blindly.

#### Likely interview questions

- What is a decorator?
- Why are nested functions used in decorators?
- Why use `functools.wraps`?
- How do decorator arguments add another closure level?
- In what order do stacked decorators run?
- How would you decorate an async function?

#### Exercises

1. Write a decorator that logs arguments and return values without changing behavior.
2. Write `@require_role("admin")` for a function receiving a user object.
3. Implement `@retry(attempts=3)` that catches only a supplied exception type.
4. Write a timing decorator that supports both synchronous and async functions.
5. Stack two decorators and write down the decoration order and call order before running it.

---

### 7. Exceptions and context managers

#### Exception flow

```python
try:
    value = int("42")
except ValueError as error:
    print(f"Invalid number: {error}")
else:
    print(f"Parsed: {value}")
finally:
    print("Always runs")
```

- `except` handles a matching failure.
- `else` runs only when the `try` block succeeds.
- `finally` runs whether the operation succeeds or fails.

Catch the narrowest exception you can handle meaningfully. Avoid `except:` because it also catches control-flow exceptions such as `KeyboardInterrupt` and `SystemExit`.

#### Custom exceptions and chaining

```python
class ConfigurationError(Exception):
    pass


def read_port(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as error:
        raise ConfigurationError(f"Invalid port: {raw!r}") from error
```

`raise ... from error` preserves the original cause while presenting a domain-specific error.

#### Context managers

A context manager guarantees setup and cleanup around a block. Files, locks, database transactions, and temporary resources are common examples.

```python
with open("events.log", encoding="utf-8") as file:
    first_line = file.readline()
```

Class-based context manager:

```python
class ManagedConnection:
    def __enter__(self):
        self.connection = connect()
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.connection.close()
        return False  # Do not suppress an exception
```

Function-based context manager:

```python
from contextlib import contextmanager
from collections.abc import Iterator


@contextmanager
def transaction(database) -> Iterator[object]:
    connection = database.connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
```

#### Likely interview questions

- `else` versus `finally` in exception handling?
- Why should exceptions be specific?
- How do you define a custom exception?
- What is exception chaining?
- What do `__enter__` and `__exit__` do?
- When should `__exit__` return `True`?

#### Exercises

1. Parse a configuration value and translate `ValueError` into a custom exception while preserving the cause.
2. Write a context manager that measures a code block's execution time.
3. Implement a temporary setting that restores the old value even when an exception occurs.
4. Write tests proving a database transaction commits on success and rolls back on failure.
5. Review a function with three broad `except Exception` blocks and narrow them appropriately.

---

### 8. Type hints and interface design

#### Mental model

Type hints describe the shape of your code for humans, IDEs, and static type checkers. Python itself does not enforce normal type hints at runtime.

```python
def normalize_name(name: str) -> str:
    return name.strip().title()

print(normalize_name(" ada "))
print(normalize_name(123))  # Runtime error only when `.strip()` is called
```

Use type hints to make interfaces easier to understand, easier to refactor, and easier to test. Avoid turning every small expression into a typing puzzle.

#### Common annotations

```python
from typing import Any

def summarize_scores(scores: list[int]) -> dict[str, float]:
    total = sum(scores)
    average = total / len(scores)
    return {"total": float(total), "average": average}


def find_user(user_id: str) -> dict[str, object] | None:
    if user_id == "missing":
        return None
    return {"id": user_id, "active": True}


def log_payload(payload: Any) -> None:
    print(payload)
```

Prefer precise types when they communicate useful constraints. Use `Any` only when the value is genuinely unknown or when typing it would add noise without improving safety.

#### `TypedDict`

Use `TypedDict` for dictionary-shaped data with known keys, especially JSON-like payloads. It remains a plain dictionary at runtime.

```python
from typing import NotRequired, TypedDict


class UserPayload(TypedDict):
    id: str
    name: str
    email: NotRequired[str]


user: UserPayload = {"id": "u1", "name": "Ada"}
```

Choose `TypedDict` when you need dictionary compatibility. Choose a class or dataclass when you need methods, validation logic, or richer behavior.

#### `dataclass`

A dataclass generates common methods such as `__init__`, `__repr__`, and `__eq__`. Use `field(default_factory=...)` for mutable defaults.

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Endpoint:
    host: str
    port: int
    tags: tuple[str, ...] = field(default_factory=tuple)


endpoint = Endpoint("localhost", 8000)
print(endpoint)
```

A frozen dataclass is useful for immutable value objects, but it is not a replacement for validation libraries when inputs are untrusted.

#### `Protocol` and duck typing

Duck typing means Python cares about what an object can do, not what it inherits from. `Protocol` lets you describe that expected behavior for static checkers.

```python
from typing import Protocol


class Cache(Protocol):
    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str) -> None: ...


class DictCache:
    def __init__(self) -> None:
        self._values: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._values.get(key)

    def set(self, key: str, value: str) -> None:
        self._values[key] = value


def read_cached(cache: Cache, key: str) -> str:
    value = cache.get(key)
    return value if value is not None else "missing"
```

Use `Protocol` when you want swappable implementations without requiring inheritance.

#### `ABC` versus `Protocol`

Abstract base classes enforce required methods at runtime when a subclass is instantiated. Protocols are mainly for static structural typing.

| Feature | Protocol | ABC |
|---|---|---|
| Main check | Static type checking | Runtime instantiation |
| Inheritance | Can be implicit | Must be explicit |
| Best fit | Flexible interfaces | Framework/plugin base classes |
| Concrete methods | Possible, but less central | Common and useful |

#### `Callable`, generics, and constrained values

Use `Callable` when a function accepts another function. Use `TypeVar` when a function or class should preserve the caller's type. Use `Literal` when a value must be one of a small set of allowed strings.

```python
from typing import Callable, Literal, TypeVar

T = TypeVar("T")
Mode = Literal["fast", "safe"]


def first(items: list[T]) -> T | None:
    return items[0] if items else None


def process(value: int, transform: Callable[[int], str], mode: Mode) -> str:
    prefix = "FAST" if mode == "fast" else "SAFE"
    return f"{prefix}: {transform(value)}"
```

For most interviews, know the basic syntax and the design reason. Advanced topics such as variance and complex generic constraints are lower priority.

#### Likely interview questions

- Do Python type hints enforce types at runtime?
- `list[str]` versus `List[str]`?
- When would you use `TypedDict` versus a dataclass?
- What is `Any`, and why can overusing it be risky?
- What is a `Protocol`, and how is it different from an ABC?
- How would you type a callback function?
- Why are type hints useful in a large codebase?

#### Exercises

1. Add complete annotations to a small untyped module and run mypy or pyright.
2. Define a `TypedDict` for an API response with one optional field.
3. Define a protocol for a cache with `get` and `set`, then implement in-memory and fake versions.
4. Write generic `last(items)` while handling the empty sequence explicitly.
5. Replace unnecessary `Any` annotations in an example with more precise types.

---

## 9. Concurrency Model - GIL, Async I/O, Threading, Multiprocessing

| Term | Meaning (Python) |
|------|------------------|
| **Concurrency** | Structuring a program as many independent tasks making progress *apparently* at once (interleaved on one core). |
| **Parallelism** | Multiple tasks literally running on multiple cores at the same instant. |
| **Async I/O** | Concurrency via an **event loop** + cooperative `await`. Non-blocking I/O, single OS thread. |
| **Threading** | Concurrency on one interpreter state, one GIL per interpreter. Good for I/O wait; limited for CPU. |
| **Multiprocessing** | One interpreter (and one GIL) **per process**. True parallelism, pays pickling + fork/spawn overhead. |

### The CPython GIL (Global Interpreter Lock)

- One lock per interpreter process ⇒ only **one bytecode executes at a time** in a given process.
- **I/O-bound** work (disk, network, `time.sleep`) **releases the GIL**, so threads *do* speed up
  I/O-bound code. **CPU-bound** pure-Python code does **not** benefit: threads add contention, not throughput.
- `multiprocessing` (and 3.14 free-threaded CPython) sidesteps the GIL by giving each worker its own interpreter/lock.

> Sources: [Concurrency overview](https://docs.python.org/3/library/concurrency.html), [GIL note in coroutines/tasks docs](https://docs.python.org/3/library/asyncio-task.html).

### Async I/O vs Threading vs Multiprocessing — the decision matrix

```text
Workload kind:
  ┌─────────────────────────────────────┐
  │ I/O-bound?  (waiting on network/disk/sleep) │
  └──────┬──────────────────────────────┘
         │ yes            │ no
  ┌──────▼───────┐        │
  │ Has an async │        │ CPU-bound?
  │ library?     │        └──────┬──────────────┘
  └──────┬───────┘               │ yes
         │ yes          │ no   │
  ┌──────▼───────┐      │      │
  │ async/await  │      │      │
  │ (single      │      │      │
  │   thread,    │      │      │
  │   event loop)│      │      │
  └──────────────┘      │      │
                        │ ┌────▼────┐
                        │ │ threads │   (releases GIL, e.g. pandas/ numpy extensions)
                        │ │ (GIL     │
                        │ │ still    │
                        │ │ applies) │
                        │ └─────────┘
                        │      OR
                        │ ┌──────────┐
                        │ │ processes │  (free-threaded Python 3.14: threads work too)
                        │ └──────────┘
```

> Source for the 3.14 free-threaded note: [asyncio and free-threaded Python](https://docs.python.org/3/library/asyncio-threading.html).

---

## Coroutines — `async def` / `await`

A coroutine is a **function whose execution can be paused** at an `await` point and resumed later by the event loop. It is *not* a callback — it looks sequential but is driven by the loop.

```python
import asyncio

async def fetch_data(seconds: float) -> float:
    print(f"[fetch] start sleep={seconds}s")
    await asyncio.sleep(seconds)          # ← yields control back to the loop
    print(f"[fetch] done sleep={seconds}s")
    return seconds * 100

async def main() -> None:
    # Two coroutines scheduled on ONE thread; they overlap while sleeping.
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    r1, r2 = await asyncio.gather(task1, task2)  # returns in ~2s, not 3s
    print("results:", r1, r2)

asyncio.run(main())
```

**Key distinctions (often probed):**

- `async def f(): ...` **defines** a coroutine function; calling `f()` **returns a coroutine object** — it does **not** start running until you `await` it or schedule it (`create_task` / `gather`).
- Forgetting to `await` a coroutine ⇒ `"coroutine 'f' was never awaited"` **RuntimeWarning** and silent no-op. This is the #1 production surprise in migrated codebases.
- Coroutines are similar to generators but add: an `await` keyword, a *single* yield type (the awaited value), and an event loop as the driver.

```python
import warnings
warnings.simplefilter("error")  # turn the silent warning into a hard error in tests
```

---

## The Event Loop

The event loop owns a single thread, a ready-queue of callbacks, and an I/O selector (`epoll`/`kqueue`/`IOCP`). Each cycle it:

1. **Selects** which sockets/handles became ready (poll).
2. Runs **ready I/O callbacks** and timer callbacks.
3. Runs **`Task` steps**: advancing coroutines one `await` segment.

```python
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.close()
```

`asyncio.run()` (3.7+) bundles `new_event_loop` + `run_until_complete` + `close` and **asserts no other loop is running** — use it as `if __name__ == "__main__":` boilerplate, **not** from an already-looping program (e.g. Jupyter / FastAPI lifespan — call `async def` directly there).

### Node.js vs CPython event loops (classic comparison table)

| Concern | Node.js | CPython `asyncio` |
|---------|---------|-------------------|
| Driver | single C++ thread; libuv | single Python thread; `selectors`/Proactor |
| I/O offload | libuv thread-pool (default 4) for fs/dns | `run_in_executor` (default `ThreadPoolExecutor`); 3.9+ `asyncio.to_thread` shortcut |
| Blocking call penalty | blocks **all** I/O | blocks **all** coroutines on the loop thread |
| CPU-bound | must `child_process` / `worker_threads` | `multiprocessing` / `concurrent.futures.ProcessPoolExecutor` |
| Scheduling fairness | cooperative, microtask queue | cooperative; `asyncio.sleep(0)` yields once |
| Debugging | `--inspect` | `PYTHONASYNCIODEBUG=1` / `loop.set_debug(True)` |

---

## Tasks, Futures, and `gather`

| Object | Role |
|--------|------|
| **Coroutine** | lazy; only runs when awaited/scheduled. |
| **Task** | a coroutine wrapped so the loop drives it each tick. Created by `create_task` / `gather` / `TaskGroup`. |
| **Future** | a low-level **promise-like** result placeholder; `asyncio` futures have states `PENDING → CANCELLED / FINISHED`. |

> `Future` here is distinct from `concurrent.futures.Future` (the thread/process one). `asyncio.run_in_executor` returns an `asyncio`-compatible awaitable, so both interop.

### `asyncio.gather` (legacy concurrency) vs `TaskGroup` (modern)

```python
# Legacy — works, but error handling is foot-gun-y.
results = await asyncio.gather(
    fetch_data(1), fetch_data(2), fetch_data(3),
    return_exceptions=True,          # otherwise first exception cancels siblings
)
for r in results:
    if isinstance(r, Exception):
        print("task failed:", r)
```

```python
# Modern — Python 3.11+ structured concurrency.
from asyncio import TaskGroup

async def fetch_or_raise(n: float) -> float:
    await asyncio.sleep(n)
    if n == 2:
        raise ValueError("boom")
    return n

async def main() -> None:
    results: list[float] = []
    async with TaskGroup() as tg:
        tg.create_task(_collect(1), tg, results)   # see helper below
    # On exit: all tasks awaited; if any raised, others are CANCELLED,
    # and the FIRST exception is re-raised here (ExceptionGroup for >1).
```

> Source: [Coroutines and tasks — `asyncio.TaskGroup`](https://docs.python.org/3/library/asyncio-task.html).

---

## Structured Concurrency — `TaskGroup` (Python 3.11+) ✅

`async with TaskGroup()` is the **recommended** way to scope background work. Semantics (architects love these because they kill whole classes of "leaked task" bugs):

- Every task created inside is **awaited** at `__aexit__` — the `with` body cannot exit before them.
- If a task raises an exception **other than** `CancelledError`, the group **cancels all siblings** and re-raises at `__aexit__`.
- If *multiple* tasks raise, you get an **`ExceptionGroup`** (`BaseExceptionGroup` for `KeyboardInterrupt`/`SystemExit`), not a swallowed second error. This fixes `gather`'s "only first exception survives" problem.
- Nesting `TaskGroup` blocks composes cleanly (the basis of structured concurrency).

```python
import asyncio
from asyncio import TaskGroup, CancelledError

async def work(name: str, delay: float) -> str:
    try:
        await asyncio.sleep(delay)
    except CancelledError:
        # group cancelled a sibling → we are cancelled too.
        print(f"{name}: cancelled mid-flight")
        raise
    return f"{name} done in {delay}s"

async def main() -> None:
    results: list[str] = []
    try:
        async with TaskGroup() as tg:
            tg.create_task(work("A", 1))
            tg.create_task(work("B", 0.2))
            tg.create_task(work("C", 0.2))
    except* Exception as eg:                     # Python 3.11+ ExceptionGroup
        print("group failures:", eg.exceptions)
    # All started tasks are guaranteed complete here.
```

### Cancellation & timeouts (`asyncio.timeout`, 3.11+)

```python
try:
    async with asyncio.timeout(3.0):           # replaces wait_for; cancels on exit
        await long_running()
except TimeoutError:
    print("aborted; group/caller cancelled children automatically")
```

### `asyncio.shield` — guard against cascade cancellation (use sparingly)

```python
res = await asyncio.shield(critical_job())
```

---

## Async I/O vs Threads vs Processes — interop with blocking code

### `asyncio.to_thread` (3.9+) — the idiomatic "blocking call lives"

This wraps a **sync** callable in the default thread pool and awaits its result. It still runs on the **GIL** (so only helps with I/O / C-extensions that release the GIL).

```python
import asyncio
from typing import Any
import requests  # blocking, but releases GIL while waiting on the socket

async def fetch_url(url: str) -> Any:
    # requests blocking call → offloaded to a worker thread
    return await asyncio.to_thread(requests.get, url, timeout=5)

# In an async service:
async def handler(urls: list[str]) -> list[Any]:
    # Each fetch_url spawns a thread on the shared pool (min(32, cpu+4) default).
    return await asyncio.gather(*(fetch_url(u) for u in urls))
```

### `run_in_executor` → process pool (CPU bound)

```python
from concurrent.futures import ProcessPoolExecutor
import asyncio

def cpu_heavy(n: int) -> int:          # pure-Python loop — GIL-bound in threads
    total = 0
    for i in range(n):
        total += i
    return total

async def main() -> None:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=4) as exe:
        # Each task → own process (own GIL) → real parallelism.
        r = await loop.run_in_executor(exe, cpu_heavy, 10_000_000)
        print("cpu result:", r)

asyncio.run(main())
```

- Each child process = **one interpreter + one GIL**. True multi-core parallelism at the cost of **pickling args/results** and **startup** latency.
- Share data via **return values** (pickled) → simplest. For streaming use `multiprocessing.Queue`/`Pipe`.
- Prefer **`fork`** spawn on Linux (fast, inherits FDs) **but** fork after threads/started servers is hazardous (copy-on-write + locks). On macOS/Windows use **`spawn`**.

> Source for process-safe queue + GIL-bypass: [multiprocessing — Process-based parallelism](https://docs.python.org/3/library/multiprocessing.html).

---

## Queues — backpressure & fan-out

### `asyncio.Queue` (async/await; **not** thread-safe)

Producer/consumer with `TaskGroup`, bounded for backpressure:

```python
import asyncio
from asyncio import Queue, TaskGroup

WORKERS = 4

async def producer(q: Queue[tuple[int, int]], n: int) -> None:
    for i in range(n):
        await q.put((i, i * i))    # blocks when q is full (maxsize)
    for _ in range(WORKERS):
        await q.put(None)          # sentinel per worker

async def worker(q: Queue, out: list) -> None:
    while True:
        item = await q.get()
        try:
            if item is None:
                break
            idx, val = item
            await asyncio.sleep(0.01)        # simulate I/O
            out.append((idx, val))
        finally:
            q.task_done()

async def main() -> None:
    q: Queue = Queue(maxsize=WORKERS * 2)   # bounded → backpressure
    out: list = []
    async with TaskGroup() as tg:
        tg.create_task(producer(q, 100))
        for _ in range(WORKERS):
            tg.create_task(worker(q, out))
    print("collected:", len(out))

asyncio.run(main())
```

### Queue selection by layer

| Primitive | Thread-safe? | Inter-process? | Use |
|-----------|:---:|:---:|-----|
| `queue.Queue` | ✅ | ❌ | thread producer↔consumer |
| `asyncio.Queue` | ❌ (loop-bound) | ❌ | coroutine producer↔consumer |
| `multiprocessing.Queue` | ✅ | ✅ | process producer↔consumer (serializes via pickle) |

> Sources: [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html), [multiprocessing.Queue](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue).

---

## Debugging & Observability

```bash
# 1. Turn on the debug mode globally
PYTHONASYNCIODEBUG=1 python app.py

# 2. In-code, per-loop
import asyncio, logging
asyncio.get_event_loop().set_debug(True)
logging.basicConfig(level=logging.DEBUG)
```

What debug mode adds:

- `"coroutine 'X' was never awaited"` → hard error/warning (catches silent no-ops).
- Detects long blocks > `loop.slow_callback_duration` (default 100ms) — reveals stray `time.sleep()` / sync HTTP in async code.
- Warns on un-GC'd coroutines and un-awaited futures.

Production hardening:

- Run on **uvloop** (`pip install uvloop`) for ~10–30% lower latency vs the stdlib selector loop (Linux/macOS only).
- Add **`TaskGroup`** task-name tracing and a **`CancelledError` logger**; log every task creation at DEBUG in staging.
- Instrument **queue depth / in-flight counters** as Prometheus-style gauges — saturation shows up as a steadily full `Queue(maxsize)`.
- Avoid the classic anti-patterns (see §10 checklist).

---

## Common Pitfalls (and how to stop them)

1. **Blocking call inside a coroutine** (`requests.get`, `time.sleep`, `cursor.execute`) freezes the entire loop thread. Detection: `PYTHONASYNCIODEBUG=1`. Fix: offload via `to_thread` / `run_in_executor`, or swap to an async lib (`aiohttp`, `aiomysql`, `psycopg[async]`).
2. **Forgetting `await`** ⇒ coroutine object created but never scheduled ⇒ silent no-op + `RuntimeWarning`.
3. **Exception swallowed by `gather(return_exceptions=True)`** then never inspected.
4. **Mixing thread-pool and event-loop primitives** incorrectly: an `asyncio.Queue` is **not** thread-safe; an `asyncio.Task` must not be `.set_result` from another thread (use `loop.call_soon_threadsafe`).
5. **Forking after threads** can deadlock locks captured in copy-on-write memory — prefer `spawn`.

---

## Interview — sample answers

**Q: "If your async service has a single event loop, how can it hit 10k RPS?"**
Async I/O overlaps the *waiting* (network/IO), not the CPU. A single-core loop can drive thousands of concurrent in-flight requests as long as per-request CPU is tiny and the loop never blocks. You still shard across **processes** (or containers) for multi-core scale and to avoid a single loop-thread bottleneck — async solves **concurrency**, not **parallelism**.

**Q: "How do you guarantee a spawned background task is always finished or cancelled?"**
Use **`TaskGroup`** (`async with`). Every `tg.create_task(...)` is awaited on exit and auto-cancelled on sibling failure — eliminating the leaked-task class of bugs that `create_task`-without-bookkeeping causes.

**Q: "When does `asyncio.gather(*coros, return_exceptions=True)` hide errors — and what replaced it?"**
`return_exceptions=True` returns exceptions as values, so a caller that doesn't iterate the results **silently loses** the failure. Modern replacement: `TaskGroup` + `except*` (PEP 654) which cancels siblings and **always** re-raises via `ExceptionGroup`.

**Q: "How to call sync, GIL-free C-extension code from async?"**
`await asyncio.to_thread(c_ext_call)` or `loop.run_in_executor(..., c_ext_call)`. Because the C function releases the GIL while blocked on I/O, the thread yields the CPU to other coroutines — threads here add concurrency (not CPU parallelism), which is exactly what async needs.

---

## Quick-reference checklist (debug your own code)

- [ ] Every `async def` is either `await`ed or scheduled (`create_task`/`gather`/`TaskGroup`).
- [ ] No blocking stdlib (`requests`, `sqlite`, `time.sleep`) in coroutine bodies.
- [ ] `asyncio.Queue` only touched from the loop thread; use `queue.Queue` for cross-thread handoff.
- [ ] Failures inside concurrent work use `TaskGroup` (not bare `gather`) so nothing is leaked or swallowed.
- [ ] CPU-bound pure-Python loops go to `ProcessPoolExecutor`, not `to_thread`.
- [ ] `PYTHONASYNCIODEBUG=1` in CI for a test run; review "long-awaited" slow-callback logs.
- [ ] Fork only before threads; otherwise `spawn` (or `forkserver`) + `if __name__ == "__main__":` guard.

---

### Sources

- [Concurrency overview](https://docs.python.org/3/library/concurrency.html)
- [Coroutines and tasks — `TaskGroup`, GIL notes on `to_thread`](https://docs.python.org/3/library/asyncio-task.html)
- [asyncio and free-threaded Python (3.14, no-GIL)](https://docs.python.org/3/library/asyncio-threading.html)
- [Queues — `asyncio.Queue`](https://docs.python.org/3/library/asyncio-queue.html)
- [multiprocessing — `Queue`, `Pipe`, GIL bypass](https://docs.python.org/3/library/multiprocessing.html)

---

### 10. Testing, mocking, and debugging

#### Test behavior, not implementation details

A useful test follows arrange, act, assert:

```python
import pytest


def divide(total: float, count: int) -> float:
    if count <= 0:
        raise ValueError("count must be positive")
    return total / count


def test_divide_returns_average() -> None:
    result = divide(10, 2)
    assert result == 5


def test_divide_rejects_zero() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        divide(10, 0)
```

#### Fixtures

Fixtures provide reusable setup and cleanup.

```python
import pytest


@pytest.fixture
def sample_users() -> list[dict[str, object]]:
    return [
        {"id": 1, "active": True},
        {"id": 2, "active": False},
    ]
```

#### Parametrization

```python
@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1", 1), ("20", 20), ("-3", -3)],
)
def test_parse_integer(raw: str, expected: int) -> None:
    assert int(raw) == expected
```

#### Mock at a boundary

Mock network, clock, filesystem, or database boundaries when a unit test should not use the real dependency. Patch the name where the code under test looks it up, not necessarily where it was originally defined.

Prefer a small fake implementing a protocol when extensive mocking starts to mirror implementation details.

#### Async tests

With `pytest-asyncio`:

```python
import pytest


@pytest.mark.asyncio
async def test_fetch() -> None:
    result = await fetch("item", 0)
    assert result == "finished item"
```

#### Debugging approach

1. Reproduce the issue reliably.
2. Reduce it to the smallest failing input.
3. Read the complete traceback from the bottom upward.
4. Inspect assumptions using a debugger, structured logs, or temporary assertions.
5. Fix the cause and add a regression test.

Know `breakpoint()`, traceback reading, logging levels, and the difference between a unit test and an integration test.

#### Likely interview questions

- What makes a good unit test?
- Fixture versus helper function?
- Mock versus fake?
- Where should `patch` be applied?
- How do you test exceptions and async functions?
- Unit, integration, and end-to-end tests: what does each prove?
- How would you debug an intermittent production failure?

#### Exercises

1. Test the happy path, invalid input, and dependency failure for one service function.
2. Parametrize ten edge cases for a parser.
3. Replace a network client with a protocol-based fake.
4. Test retry behavior without actually waiting by patching the sleep boundary.
5. Debug a failing function using `breakpoint()` and write a regression test.

---

### 11. Coding problems and complexity

#### What interviewers assess

They are usually evaluating more than the final answer:

- Did you clarify inputs and edge cases?
- Did you choose the right collection?
- Is the solution correct and readable?
- Can you state time and space complexity?
- Can you improve a brute-force solution?
- Can you test your own code with examples?

#### A reliable interview method

1. Restate the problem and ask about constraints.
2. Give one small example, including an edge case.
3. Explain a straightforward approach.
4. Improve it if the constraints require it.
5. Write readable code with meaningful names.
6. Dry-run the code aloud.
7. State time and space complexity.

#### Essential patterns

##### Frequency map

```python
from collections import Counter


def first_unique(text: str) -> str | None:
    counts = Counter(text)
    return next((character for character in text if counts[character] == 1), None)
```

##### Set for seen values

```python
def has_duplicate(values: list[int]) -> bool:
    seen: set[int] = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False
```

##### Two pointers

Useful for sorted arrays, palindrome checks, and in-place partitioning.

##### Sliding window

Useful for contiguous subarrays/substrings, especially longest/shortest windows satisfying a condition.

##### Stack and queue

Use a list as a stack with `append`/`pop`. Use `deque` as a queue with `append`/`popleft`.

##### Heap

Use `heapq` for top-k, scheduling, and repeatedly retrieving the smallest item.

#### Complexity worth memorizing

| Operation | Average time |
|---|---|
| List index | O(1) |
| List append/pop at end | Amortized O(1) |
| List membership | O(n) |
| Insert/delete at list front | O(n) |
| Dict/set lookup, insert, delete | Average O(1) |
| Sorting | O(n log n) |
| Heap push/pop | O(log n) |
| `deque` append/popleft | O(1) |

#### Core exercise set

Solve these without an IDE autocomplete first, then add tests:

1. Reverse the words in a sentence while normalizing spaces.
2. Find the first non-repeating character.
3. Remove duplicates while preserving order.
4. Check whether two strings are anagrams.
5. Return the top-k most frequent items.
6. Merge overlapping intervals.
7. Flatten a nested list by one level, then as an arbitrary-depth generator.
8. Group records by a selected key.
9. Implement a fixed-capacity LRU cache using `OrderedDict` or explain a manual design.
10. Implement a producer-consumer queue.
11. Parse a log stream and count errors by service.
12. Implement a retry decorator with backoff.
13. Implement a per-user in-memory rate limiter.
14. Process records in lazy batches.
15. Find the longest substring without repeated characters.

For senior roles, expect follow-ups about invalid input, memory limits, thread safety, observability, and how the in-memory solution changes in a distributed system.

---

## Good To Know

### 12. Files, JSON, serialization, and parsing

#### Files

When opening a file explicitly, use a context manager and normally specify text encoding. Convenience methods such as `Path.read_text()` open and close the file internally.

```python
from pathlib import Path

path = Path("config.json")
text = path.read_text(encoding="utf-8")
```

For very large files, iterate line by line instead of calling `read()` or `readlines()`.

```python
with open("events.log", encoding="utf-8") as file:
    for line in file:
        process(line)
```

#### JSON

```python
import json

payload = '{"id": 42, "active": true}'
data = json.loads(payload)
encoded = json.dumps(data, indent=2, sort_keys=True)
```

Know the distinction: `loads` parses a `str`, `bytes`, or `bytearray`; `dumps` always returns a `str`. `load` reads from a file-like object, while `dump` writes text to one.

Validate external data before relying on its fields and types.

#### Pickle safety

`pickle` preserves Python-specific object structures, but loading a pickle can execute arbitrary code. Never unpickle untrusted or unauthenticated data.

#### Parsing

Prefer a real parser or structured API for structured formats. Avoid fragile string splitting when CSV, JSON, URL, date/time, or shell syntax has a standard parser.

#### Likely interview questions

- Why use `with open(...)`?
- `read`, `readline`, and iteration over a file?
- `json.load` versus `json.loads`?
- Why is pickle unsafe for untrusted data?
- How would you process a 20 GB log file?

#### Exercises

1. Stream a large JSON Lines file and report invalid rows without stopping the entire job.
2. Merge two configuration files with explicit override precedence.
3. Parse CSV with quoted commas using the `csv` module rather than `split(",")`.
4. Write results atomically using a temporary file followed by replacement.
5. Design a serializer for a dataclass containing a `datetime` and explain the format choice.

---

### 13. Memory management and performance

#### References and garbage collection

CPython primarily uses reference counting: an object's reference count changes as references are created or removed, and an object can usually be reclaimed when the count reaches zero. A cyclic garbage collector handles unreachable reference cycles.

This is an implementation-level explanation, not a guarantee for every Python interpreter. Do not build normal application logic around an exact destruction time; use context managers for deterministic resource cleanup.

#### Measure before optimizing

Use the right tool for the question:

- `timeit` for small timing comparisons
- `cProfile` for function-level CPU profiling
- `tracemalloc` for Python memory allocation tracing
- application metrics and tracing for production bottlenecks

#### Common practical improvements

- Select the correct data structure.
- Avoid repeated work inside loops.
- Stream data with generators when full materialization is unnecessary.
- Batch expensive I/O calls.
- Use built-ins and library operations implemented efficiently.
- Profile before changing clear code into clever code.

```python
# Rebuilds a set for every item: unnecessary work
matches = [item for item in items if item in set(allowed)]

# Build once
allowed_set = set(allowed)
matches = [item for item in items if item in allowed_set]
```

#### Likely interview questions

- How does Python manage memory at a high level?
- What are reference cycles?
- How would you investigate a memory increase?
- Generator versus list memory usage?
- How do you profile slow Python code?
- Why is algorithm choice often more important than micro-optimization?

#### Exercises

1. Use `timeit` to compare list and set membership at different sizes.
2. Use `tracemalloc` to compare a materialized pipeline with a generator pipeline.
3. Profile a deliberately slow text-processing function and improve the measured bottleneck.
4. Find and remove repeated O(n) work inside a loop.
5. Explain why `sys.getsizeof(container)` does not necessarily include all nested objects.

---

### 14. Environments and packaging

#### Package basics

- A package groups modules, commonly in a directory.
- `__init__.py` commonly marks and initializes a regular package, although namespace packages can exist without it.
- Prefer clear absolute imports in application code, such as `from project.services.users import UserService`.

#### Virtual environments and project metadata

A virtual environment provides an isolated package installation location and command environment while normally sharing the base Python installation and standard library.

Modern projects commonly define metadata and dependencies in `pyproject.toml`. Tools such as `pip`, `uv`, or Poetry can install/manage dependencies; understand the tool used by the target company rather than trying to master every tool.

Know the purpose of:

- direct dependencies versus transitive dependencies
- version constraints and lock files
- editable installs during development
- reproducible environments

#### Likely interview questions

- Why use a virtual environment?
- What belongs in `pyproject.toml`?
- Direct dependency versus transitive dependency?
- What is the purpose of a lock file?

#### Exercises

1. Turn two related modules into a small package with clear absolute imports.
2. Add a `pyproject.toml` and install the package in editable mode.
3. Create a fresh virtual environment and prove that its installed packages differ from another environment.
4. Write a CLI entry point that does no expensive work during import.
5. Explain how you would pin dependencies for an application versus declare compatible ranges for a library.

---

### 15. Useful standard-library tools

You do not need to memorize the whole standard library. Recognize these tools and know the problem each solves.

#### `functools`

- `wraps`: preserve decorated-function metadata
- `lru_cache`/`cache`: memoize pure-ish calls
- `partial`: pre-fill some function arguments
- `reduce`: cumulative reduction, although a loop is often clearer

```python
from functools import lru_cache


@lru_cache(maxsize=256)
def load_schema(name: str) -> str:
    return expensive_lookup(name)
```

Ask about cache invalidation, memory growth, argument hashability, and whether stale data is acceptable.

#### `itertools`

- `chain`: iterate over multiple iterables as one
- `islice`: slice an iterator lazily
- `groupby`: group adjacent items sharing a key
- `product`: Cartesian product
- `combinations`: combinations without replacement

`groupby` groups consecutive items with the same key. Sort first only when all items sharing a key must form one group; sorting may destroy meaningful input order.

#### `collections`

- `Counter`: frequencies
- `defaultdict`: default values for missing keys
- `deque`: efficient work at both ends
- `OrderedDict`: explicit ordering operations; still useful for LRU-style behavior
- `ChainMap`: layered mappings

#### Other useful modules

- `heapq`: min-heap/top-k problems
- `bisect`: binary search/insertion in a sorted list
- `pathlib`: filesystem paths
- `datetime` and `zoneinfo`: time and time zones
- `enum`: named finite choices
- `contextlib`: context-manager helpers

#### Likely interview questions

- How would you implement memoization?
- How does `groupby` handle consecutive keys, and when should input be sorted first?
- Efficient top-k elements?
- `deque` versus list for a queue?
- Why prefer timezone-aware datetimes?

#### Exercises

1. Build an LRU cache with `OrderedDict`, then compare it with `functools.lru_cache`.
2. Return the top five events using `heapq` without sorting the entire input.
3. Lazily combine and batch several iterables using `chain` and `islice`.
4. Group sorted records with `itertools.groupby`, then demonstrate the result with unsorted input.
5. Convert an aware timestamp between two zones using `zoneinfo`.

---

## Practice Resources

### YouTube learning links

These are best used after reading the matching section and before doing its exercises.

| Topic | Video | How to use it |
|---|---|---|
| Broad intermediate review | [Intermediate Python Programming Course - freeCodeCamp](https://www.youtube.com/watch?v=HGOBQPFzWKo) | Use timestamps; do not watch the entire course before coding |
| OOP | [Python OOP Tutorial 1: Classes and Instances - Corey Schafer](https://www.youtube.com/watch?v=ZDa-Z5JzLYM) | Continue through the linked OOP series for class variables, inheritance, and dunder methods |
| Generators | [Python Tutorial: Generators - Corey Schafer](https://www.youtube.com/watch?v=bD05uGo_sVI) | Rebuild each example without copying |
| Decorators | [Python Tutorial: Decorators - Corey Schafer](https://www.youtube.com/watch?v=FsAPt_9Bf3U) | Implement `timed` and `retry` immediately afterward |
| Context managers | [Python Tutorial: Context Managers - Corey Schafer](https://www.youtube.com/watch?v=iba-I4CrmyA) | Build both class-based and `contextmanager` versions |
| Type hints | [Python Typing: Type Hints and Annotations - Tech With Tim](https://www.youtube.com/watch?v=QORvB-_mbZ0) | Type one of your existing scripts while watching |
| Async fundamentals | [Python Asynchronous Programming: asyncio and async/await - Tech With Tim](https://www.youtube.com/watch?v=t5Bo1Je9EmE) | Run sequential and concurrent versions side by side |
| Async deeper practice | [Asyncio in Python: Full Tutorial - Tech With Tim](https://www.youtube.com/watch?v=Qb9s3UiMSTA) | Focus on tasks, synchronization, and realistic examples |
| Unit testing | [Python Unit Testing with unittest - Corey Schafer](https://www.youtube.com/watch?v=6tNS--WetLI) | Concepts transfer to pytest; rewrite examples using pytest |

Video syntax may use an older Python release, but the core concepts remain applicable. Prefer current syntax from this handbook and the current official Python documentation.

### Python coding-practice links

#### Best starting choices

- [HackerRank Python domain](https://www.hackerrank.com/domains/python): topic-based drills for collections, exceptions, classes, decorators, and language syntax.
- [Exercism Python track](https://exercism.org/tracks/python/exercises): test-driven exercises with community solutions and optional mentoring.
- [Practice Python](https://www.practicepython.org/): short beginner-to-intermediate exercises; useful for quick daily repetitions.

#### Interview problem practice

- [LeetCode problem set](https://leetcode.com/problemset/): use Python and focus first on arrays, strings, hash tables, stacks, queues, heaps, and sliding windows.
- [HackerRank interview preparation kit](https://www.hackerrank.com/interview/interview-preparation-kit): structured algorithm practice.
- [Codewars Python](https://www.codewars.com/kata/search/python): short kata with many community solutions; compare solutions only after submitting yours.

#### Topic exercises with solutions

- [PYnative Python exercises](https://pynative.com/python-exercises-with-solutions/): exercises grouped by topic, with solutions for checking after attempting.
- [Exercism Python repository](https://github.com/exercism/python): exercise instructions and tests that can be run locally.
- [Corey Schafer code snippets](https://github.com/CoreyMSchafer/code_snippets): source code accompanying many of the linked videos.

#### Official references

- [Python tutorial](https://docs.python.org/3/tutorial/)
- [Python standard library](https://docs.python.org/3/library/)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [pytest documentation](https://docs.pytest.org/)

#### Recommended practice mapping

| Handbook sections | Practice source |
|---|---|
| 1-3 | HackerRank Python basic data types, strings, sets, built-ins, and functionals |
| 4 | Exercism classes exercises; build the `Task` and `Endpoint` exercises locally |
| 5-7 | Local exercises first, then HackerRank decorators and iterables-related challenges |
| 8 | Add type hints to three completed exercises and run a static checker |
| 9 | Build local concurrency exercises; most algorithm sites do not test async design well |
| 10 | Add pytest tests to every local exercise |
| 11 | LeetCode easy/medium and HackerRank interview kit |
| 12-15 | Build one log-processing command-line program using JSON, generators, tests, and profiling |

---

### Final mock-round checklist

Before an interview, verify that you can do these without notes:

- Explain mutability, references, `is`/`==`, shallow/deep copy, and mutable defaults.
- Choose between list, tuple, set, dictionary, `deque`, and `Counter`.
- Use comprehensions, unpacking, `enumerate`, `zip`, and `sorted(key=...)`.
- Explain LEGB, closures, `*args`, `**kwargs`, and keyword-only arguments.
- Explain first-import module execution, `sys.modules`, the main guard, and circular-import risks.
- Design a class with a dataclass, class method, property, and useful dunder methods.
- Write a generator and explain one-pass lazy evaluation.
- Write a decorator using a closure and `functools.wraps`.
- Write a custom context manager and preserve exception information.
- Add useful type hints and explain `Protocol`, `TypedDict`, and basic generics.
- Select threads, processes, or asyncio for a workload and justify the choice.
- Write concurrent async code with task lifetime, timeout, cancellation, and bounded concurrency.
- Write pytest tests using parametrization, fixtures, and a dependency fake/mock.
- Solve common hash-map, two-pointer, sliding-window, stack, queue, and heap problems.
- State time and space complexity and test edge cases aloud.

#### A realistic readiness test

Run a 60-minute mock round:

1. 15 minutes: answer five concept questions from Sections 1-8.
2. 25 minutes: solve one easy-to-medium coding problem and test it.
3. 10 minutes: answer one concurrency scenario.
4. 10 minutes: review a short function for correctness, readability, typing, and test gaps.

You are ready when your explanations are clear and your code is correct and readable. Perfect recall of obscure Python internals is not required.




