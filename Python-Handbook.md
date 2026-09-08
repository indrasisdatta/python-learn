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

### MUST know

1. [Core data model: objects, mutability, identity, and copying](#1-core-data-model-objects-mutability-identity-and-copying)
2. [Collections, comprehensions, and essential built-ins](#2-collections-comprehensions-and-essential-built-ins)
3. [Functions, arguments, scope, and closures](#3-functions-arguments-scope-and-closures)
4. [Object-oriented Python and the Python data model](#4-object-oriented-python-and-the-python-data-model)
5. [Iterables, iterators, and generators](#5-iterables-iterators-and-generators)
6. [Decorators](#6-decorators)
7. [Exceptions and context managers](#7-exceptions-and-context-managers)
8. [Type hints and interface design](#8-type-hints-and-interface-design)
9. [Concurrency: threads, processes, and asyncio](#9-concurrency-threads-processes-and-asyncio)
10. [Testing, mocking, and debugging](#10-testing-mocking-and-debugging)
11. [Coding problems and complexity](#11-coding-problems-and-complexity)

### GOOD TO KNOW

12. [Files, JSON, serialization, and parsing](#12-files-json-serialization-and-parsing)
13. [Memory management and performance](#13-memory-management-and-performance)
14. [Environments and packaging](#14-environments-and-packaging)
15. [Useful standard-library tools](#15-useful-standard-library-tools)

### Practice resources

1. [YouTube learning links](#youtube-learning-links)
2. [Python coding-practice links](#python-coding-practice-links)
3. [Final mock-round checklist](#final-mock-round-checklist)

---

## What is actually required?

No, every item in a large "Python mastery" roadmap is not required for one Python interview round.

### MUST know

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

### GOOD TO KNOW

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

# MUST Know

## 1. Core data model: objects, mutability, identity, and copying

### Mental model

Python variables are names bound to objects. Assignment does not normally copy an object; it creates another reference to it.

```python
first = [1, 2]
second = first
second.append(3)

print(first)          # [1, 2, 3]
print(first is second)  # True
```

`first` and `second` refer to the same list. The list changed; neither variable was "copied."

### Mutable and immutable objects

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

### `==` versus `is`

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

### Shallow versus deep copy

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

### Function arguments use object sharing

Python passes object references by assignment. A function can mutate an object it receives, but rebinding the local parameter does not rebind the caller's variable.

```python
def change(values: list[int]) -> None:
    values.append(4)       # Mutates the caller's list
    values = [99]          # Rebinds only the local name


numbers = [1, 2, 3]
change(numbers)
print(numbers)  # [1, 2, 3, 4]
```

### Classic trap: mutable default arguments

Default argument objects are created once when the function is defined, not once per call.

```python
def add_event(event: str, events: list[str] | None = None) -> list[str]:
    if events is None:
        events = []
    events.append(event)
    return events
```

### Likely interview questions

- What is the difference between `is` and `==`?
- Why is a mutable default argument dangerous?
- What changes when a list is passed to a function?
- What is the difference between a shallow and deep copy?
- Can a tuple contain a list? Is that tuple hashable?

### Exercises

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

## 2. Collections, comprehensions, and essential built-ins

### Choosing the correct collection

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

### Comprehensions

Use comprehensions for short transformations and filtering. Prefer a normal loop when the logic has several branches or side effects.

```python
scores = {"a": 82, "b": 49, "c": 91}
passed = {name: score for name, score in scores.items() if score >= 50}
```

### Unpacking

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

### Essential built-ins

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

### Common collection tools

```python
from collections import Counter, defaultdict, deque

counts = Counter("mississippi")

groups: defaultdict[str, list[int]] = defaultdict(list)
groups["odd"].append(3)

queue = deque(["job-1", "job-2"])
next_job = queue.popleft()
```

Use `deque.popleft()` for an efficient queue. Removing index 0 from a list is O(n).

### Likely interview questions

- When would you choose a tuple over a list?
- Why is a set faster for membership checks?
- Are dictionaries ordered?
- How do you remove duplicates while preserving order?
- What is the difference between `list.sort()` and `sorted()`?
- When is a comprehension too complex?

### Exercises

1. Remove duplicates from a list while preserving first-seen order.
2. Count words case-insensitively and return the three most common words.
3. Group a list of employees by department with `defaultdict`.
4. Join two lists, `names` and `scores`, into a dictionary using `zip`.
5. Sort API records by descending priority, then ascending creation time.
6. Implement a queue twice: once with a list and once with `deque`; explain the complexity difference.

---

## 3. Functions, arguments, scope, and closures

### Functions are objects

Functions can be assigned to names, stored in collections, passed to other functions, and returned from functions.

```python
from collections.abc import Callable


def apply(value: int, operation: Callable[[int], int]) -> int:
    return operation(value)


def double(value: int) -> int:
    return value * 2


print(apply(5, double))  # 10
```

### Positional, keyword, and constrained arguments

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

### `*args` and `**kwargs`

```python
def log_event(event: str, *tags: str, **metadata: object) -> None:
    print(event, tags, metadata)


log_event("login", "security", "user", user_id=42, success=True)
```

Use them when forwarding flexible arguments or building a genuinely flexible API. Do not use them just to avoid designing a clear signature.

### LEGB scope

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

### Late binding in closures

Closures look up captured variables when called, which can surprise people in loops.

```python
functions = [lambda value=i: value for i in range(3)]
print([function() for function in functions])  # [0, 1, 2]
```

The default parameter captures the current value of `i` during each iteration.

### Modules, imports, and the main guard

A module is normally one `.py` file. Importing it executes its top-level code the first time in a process and caches the module object in `sys.modules`; later imports normally reuse that object.

Keep expensive work and surprising side effects out of module-level code. Circular imports often indicate that responsibilities should move to a lower-level module or that a dependency boundary needs redesigning.

```python
def main() -> None:
    print("run application")


if __name__ == "__main__":
    main()
```

The main guard prevents `main()` from running merely because another module imports the file. It is also important when starting child processes on platforms that import the main module in the new process.

### Likely interview questions

- Explain LEGB.
- What is a closure and where is it useful?
- What is the difference between `global` and `nonlocal`?
- Explain `*args` and `**kwargs`.
- What are positional-only and keyword-only arguments?
- Are lambdas different from normal functions?
- What happens the first time a module is imported?
- What does `if __name__ == "__main__"` prevent?
- Why do circular imports happen, and how would you redesign them?

### Exercises

1. Write `make_multiplier(factor)` that returns a function multiplying by `factor`.
2. Fix a loop that creates three callbacks but accidentally returns the final loop value from all three.
3. Write a function whose `timeout` and `retries` parameters must be supplied by keyword.
4. Write `compose(f, g)` so `compose(f, g)(x)` returns `f(g(x))`.
5. Explain why excessive `global` state makes testing and concurrency harder.
6. Split a small script into two modules while keeping execution behind a main guard.

---

## 4. Object-oriented Python and the Python data model

### Classes and instances

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

### Instance, class, and static methods

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

### Inheritance, MRO, and `super()`

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

### Dunder methods

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

### Dataclasses and properties

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

### Likely interview questions

- Class variable versus instance variable?
- `@classmethod` versus `@staticmethod`?
- What does `super()` do?
- Composition versus inheritance?
- `__str__` versus `__repr__`?
- What does `@dataclass` generate?
- What makes an object hashable?

### Exercises

1. Build a `Task` dataclass with `id`, `priority`, and `created_at`, then sort tasks.
2. Add value-based equality and a useful representation to a small class.
3. Implement a `Client.from_url()` alternative constructor.
4. Refactor an inheritance design into composition and explain why it is easier to test.
5. Create an immutable, hashable `Coordinate` dataclass that can be a dictionary key.

---

## 5. Iterables, iterators, and generators

### Iterable versus iterator

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

### Generators and lazy evaluation

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

### Generator expressions

```python
total = sum(number * number for number in range(1_000_000))
```

The expression supplies values to `sum` lazily instead of first creating a million-element list.

### One-pass behavior

An iterator is normally consumed once.

```python
generator = (value * 2 for value in range(3))
print(list(generator))  # [0, 2, 4]
print(list(generator))  # []
```

### `yield from`

`yield from iterable` delegates iteration to another iterable.

```python
def flatten(groups: list[list[int]]):
    for group in groups:
        yield from group
```

### Likely interview questions

- Iterable versus iterator?
- What does `yield` do?
- Generator versus list: what are the trade-offs?
- Why can a generator be exhausted?
- What happens when `next()` has no more values?
- When would lazy evaluation be a bad choice?

### Exercises

1. Write `countdown(start)` as a generator.
2. Write a generator that reads a large text file one non-empty line at a time.
3. Create a custom `RangeLike` iterator without using `range` internally.
4. Implement lazy pagination that requests the next page only when needed.
5. Compare the approximate memory used by a list comprehension and generator expression for one million integers.

---

## 6. Decorators

### Mental model

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

### A practical decorator

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

### Decorator with arguments

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

### Likely interview questions

- What is a decorator?
- Why are nested functions used in decorators?
- Why use `functools.wraps`?
- How do decorator arguments add another closure level?
- In what order do stacked decorators run?
- How would you decorate an async function?

### Exercises

1. Write a decorator that logs arguments and return values without changing behavior.
2. Write `@require_role("admin")` for a function receiving a user object.
3. Implement `@retry(attempts=3)` that catches only a supplied exception type.
4. Write a timing decorator that supports both synchronous and async functions.
5. Stack two decorators and write down the decoration order and call order before running it.

---

## 7. Exceptions and context managers

### Exception flow

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

### Custom exceptions and chaining

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

### Context managers

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

### Likely interview questions

- `else` versus `finally` in exception handling?
- Why should exceptions be specific?
- How do you define a custom exception?
- What is exception chaining?
- What do `__enter__` and `__exit__` do?
- When should `__exit__` return `True`?

### Exercises

1. Parse a configuration value and translate `ValueError` into a custom exception while preserving the cause.
2. Write a context manager that measures a code block's execution time.
3. Implement a temporary setting that restores the old value even when an exception occurs.
4. Write tests proving a database transaction commits on success and rolls back on failure.
5. Review a function with three broad `except Exception` blocks and narrow them appropriately.

---

## 8. Type hints and interface design

# Python Type Hints & Interface Design — Detailed Notes (Topics 3–15)

> Organized by priority (🔴 Must-know → 🟢 Nice-to-have). Each topic includes a practical example — many tied to Gen AI / LLM workloads since that's your target domain.

---

## 🔴 3. `TypedDict` — Typed Dictionaries

**What:** A way to give a dictionary a fixed set of keys, each with its own type. Behaves like a `dict` at runtime but gives IDE/type-checker support.

**Why it matters for interviews:** Often contrasted with `dataclass` and `NamedTuple`. Interviewers ask: "when would you use TypedDict over a dataclass?" Answer: when you're working with JSON-like data (APIs, configs, LLM outputs) and want lightweight, dict-compatible structures.

**Gen AI angle:** Perfect for modelling structured LLM responses, tool-call arguments, and prompt templates.

```python
from typing import TypedDict, NotRequired

# Simple TypedDict — all keys required
class LLMConfig(TypedDict):
    model: str
    temperature: float
    max_tokens: int

# With optional keys (Python 3.11+) or NotRequired (3.10+)
class LLMResponse(TypedDict):
    content: str
    tool_calls: list[str]
    refusal: NotRequired[str]   # may be absent

# Usage — static type checker validates keys
config: LLMConfig = {"model": "gpt-4o", "temperature": 0.7, "max_tokens": 1024}
# config["timeout"] = 30  # ← Type error! 'timeout' is not a key

# Parsed JSON from an API becomes a LLMResponse
response: LLMResponse = {"content": "Hello", "tool_calls": []}
```

**Key distinction:** `TypedDict` is a *type hint only* — no runtime enforcement, no methods. Use it when you need dict semantics with type safety.

---

## 🔴 4. `dataclass` — Data Classes

**What:** A decorator that auto-generates `__init__`, `__repr__`, `__eq__`, and more. Designed for "data containers" — classes whose primary purpose is storing data.

**Why it matters for interviews:** One of the most-used decorators in real Python. Interviewers expect you to know `@dataclass` vs `NamedTuple` vs `TypedDict` vs regular class.

**Gen AI angle:** Model configurations, hyperparameter containers, dataset records, embedding metadata.

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class ModelConfig:
    """Configuration for an LLM call."""
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.95

    # Class-level constant — not an instance field
    SUPPORTED_MODELS: ClassVar[list[str]] = ["gpt-4o", "claude-3.5", "llama-3"]

    # Mutable default — use field(default_factory=...)
    stop_sequences: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be in [0, 2]")

config = ModelConfig(model_name="gpt-4o", temperature=0.5)
print(config)  # ModelConfig(model_name='gpt-4o', temperature=0.5, ...)
```

**When to choose over TypedDict:**
- You need methods or logic attached to the data
- You want immutability (`@dataclass(frozen=True)`)
- You need `__post_init__` validation
- You want `__eq__` by value, not identity

**Frozen dataclass (interview favorite):**
```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # ← FrozenInstanceError — immutable, hashable!
hash(p)  # works because frozen=True adds __hash__
```

---

## 🔴 5. `Protocol` — Structural Subtyping (Duck Typing Done Right)

**What:** A way to define *interfaces by behavior* rather than by inheritance. A class satisfies a `Protocol` if it has the required methods/attributes — regardless of whether it explicitly inherits from it.

**Why it matters for interviews:** This is the "advanced typing" interview topic. Interviewers ask: "How is Protocol different from ABC? When would you use it?"

**Gen AI angle:** Defining interfaces for LLM clients, embedding stores, vector databases — anything where you want to swap implementations.

```python
from typing import Protocol, runtime_checkable

# A protocol — any class with an embed() method satisfies this
class EmbeddingEngine(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def batch_embed(self, texts: list[str]) -> list[list[float]]: ...

# These are COMPLETELY different classes — no common base!
class OpenAIEmbedder:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]  # actual API call

    def batch_embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]

class FakeEmbedder:  # Used in tests — no inheritance!
    def embed(self, text: str) -> list[float]:
        return [0.0] * 1536

    def batch_embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 1536 for _ in texts]

def search(query: str, engine: EmbeddingEngine, docs: list[str]) -> str:
    """Works with ANY EmbeddingEngine — OpenAI, Fake, local, etc."""
    q_vec = engine.embed(query)
    # ... similarity search ...
    return "result"

# Polymorphism without inheritance
engine: EmbeddingEngine = FakeEmbedder()  # ← Static checker is happy
search("hello", engine, ["doc1", "doc2"])
```

**`@runtime_checkable` variant:** Makes `isinstance(obj, MyProtocol)` work at runtime (checks only *methods/attributes*, not inheritance).

```python
@runtime_checkable
class Speakable(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "Woof"

isinstance(Dog(), Speakable)  # True — structural check!
```

`@runtime_checkable`only Checks Method & Attribute Existence (Not Signatures or Return Types)

---

## 🔴 6. Duck Typing vs Protocol

**Duck typing (dynamic):** "If it walks like a duck and quacks like a duck, it's a duck." No type hints, no errors until runtime.

**Protocol (static):** Same philosophy, but with static type checking. Catches mismatches at *development time*.

```python
# --- Duck typing (no types, runtime errors only) ---
def process(obj):
    return obj.serialize()  # AttributeError if obj has no serialize()

process(42)  # ← Fails at runtime: 'int' has no attribute 'serialize'

# --- Protocol (static checking, same flexibility) ---
class Serializable(Protocol):
    def serialize(self) -> bytes: ...

def process(obj: Serializable) -> bytes:
    return obj.serialize()

process(42)  # ← Type checker catches this BEFORE runtime!
```

**Interview answer:** "Duck typing gives us flexibility at runtime; Protocol gives us the same flexibility with compile-time safety. Use Protocol when you're building public APIs or large codebases where catching errors early matters."

**Practical Gen AI example:**
```python
# Tool-calling protocol — any LLM provider that supports tool calling
class ToolCallable(Protocol):
    def invoke_tool(self, name: str, args: dict) -> str: ...

# OpenAI client, Anthropic client, local mock — all work
def execute_agent(llm: ToolCallable, task: str) -> str:
    result = llm.invoke_tool("search", {"query": task})
    return f"Agent result: {result}"
```

Python’s built-in syntax relies heavily on duck typing through Dunder (Magic) Methods:

 - Iteration `(for x in obj)`: Python doesn't require obj to be a list or set. It only checks if obj implements the `__iter__()` or `__getitem__()` method.

 - Length `(len(obj))`: Python checks if obj implements `__len__()`.

 - Context Manager (with obj): Python checks if obj implements `__enter__()` and `__exit__()`.

Note:
 - Duck Typing = Default Python runtime behavior. Zero imports required.

 - `typing.Protocol` = Opt-in extra tool. Used only when you want static type checkers (mypy, IDEs) to catch structural bugs before running the code.

---

## 🔴 7. ABC (Abstract Base Classes) — Formal Interfaces

**What:** The `abc` module lets you define *enforced* interfaces. Subclasses **must** implement abstract methods or they cannot be instantiated.

**Why it matters for interviews:** Often contrasted with Protocol. Key distinction: ABC enforces at *instantiation time* (runtime); Protocol enforces at *type-check time* (static).

**Gen AI angle:** Plugin architectures, model providers, data loaders — where you want hard enforcement that implementations exist.

```python
from abc import ABC, abstractmethod
from typing import list

class BaseLLMProvider(ABC):
    """Every LLM provider MUST implement these."""

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate a completion."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        pass

    # Concrete method — subclasses inherit for free
    def health_check(self) -> bool:
        try:
            self.generate("ping", max_tokens=1)
            return True
        except Exception:
            return False

# --- Concrete implementation ---
class OpenAIProvider(BaseLLMProvider):
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        return f"[OpenAI] {prompt[:20]}..."  # actual API call

    def get_model_name(self) -> str:
        return "gpt-4o"

# --- THIS WOULD FAIL at instantiation ---
class BrokenLLM(BaseLLMProvider):
    pass  # Forgot to implement generate() and get_model_name()

# BrokenLLM()  # ← TypeError: Can't instantiate abstract class BrokenLLM

provider: BaseLLMProvider = OpenAIProvider()
print(provider.health_check())  # True (inherited concrete method)
```

**Protocol vs ABC — the interview question:**

| Feature | Protocol | ABC |
|---|---|---|
| Enforcement | Static (type checker) | Runtime (instantiation) |
| Inheritance | Implicit (structural) | Explicit (`class Foo(Base)`) |
| Methods | Only signatures | Can have concrete implementations |
| Multiple inheritance | Yes (any number of protocols) | Limited |
| Use case | Duck typing with safety | Plugin/framework APIs |

---

## 🔴 8. Dependency Injection (DI)

**What:** Instead of a class creating its own dependencies (e.g., an LLM client), you *inject* them from outside — typically via the constructor.

**Why it matters for interviews:** One of the top 3 design patterns asked about. Enables testing, swapping implementations, and clean separation of concerns.

**Gen AI angle:** Swap between OpenAI / Anthropic / local models without changing your application logic. Mock the LLM in tests.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- The dependency interface ---
class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass

# --- Real implementation ---
class OpenAIClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return "[OpenAI API] response to: " + prompt

class AnthropicClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return "[Anthropic API] response to: " + prompt

# --- Fake for testing ---
class FakeLLMClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return "fake response"

# --- The application class that DEPENDS on the interface ---
@dataclass
class ChatBot:
    client: LLMClient  # ← Injected dependency, not created here
    system_prompt: str = "You are a helpful assistant."

    def ask(self, question: str) -> str:
        prompt = f"{self.system_prompt}\n\nQuestion: {question}"
        return self.client.complete(prompt)

# --- Dependency injection in practice ---
# Production: use real client
bot = ChatBot(client=OpenAIClient())
print(bot.ask("What is Python?"))

# Testing: inject fake — no network call needed!
test_bot = ChatBot(client=FakeLLMClient())
assert test_bot.ask("test") == "fake response"
```

**Interview tip:** DI is the #1 reason to use Protocol or ABC. It's the glue between the interface layer and the implementation layer.

---

## 🔴 9. Composition over Inheritance

**What:** Build complex objects by *composing* simpler ones (has-a relationship) rather than *inheriting* from them (is-a relationship). Favored in modern Python design.

**Why it matters for interviews:** "When would you use composition vs inheritance?" is a classic OOP question. Composition is more flexible, avoids fragile base class problems, and aligns with SOLID principles.

**Gen AI angle:** Agents are composed of tools, memory, and planners — not inherited from a single base class.

```python
from dataclasses import dataclass
from typing import list

# --- Small, focused components ---
@dataclass
class Memory:
    history: list[str] = field(default_factory=list)

    def add(self, msg: str) -> None:
        self.history.append(msg)

    def get_context(self, last_n: int = 5) -> str:
        return "\n".join(self.history[-last_n:])

@dataclass
class ToolBox:
    tools: list[str] = field(default_factory=list)

    def register(self, tool_name: str) -> None:
        self.tools.append(tool_name)

    def has_tool(self, name: str) -> bool:
        return name in self.tools

@dataclass
class Retriever:
    index_name: str = "default"

    def search(self, query: str) -> list[str]:
        return [f"doc about {query}"]

# --- Agent COMPOSES these, rather than inheriting ---
@dataclass
class Agent:
    memory: Memory        # has-a: Agent HAS Memory
    tools: ToolBox        # has-a: Agent HAS ToolBox
    retriever: Retriever  # has-a: Agent HAS Retriever
    model_name: str = "gpt-4o"

    def run(self, query: str) -> str:
        context = self.memory.get_context()
        docs = self.retriever.search(query)
        if self.tools.has_tool("web_search"):
            docs.append("web result")
        return f"Answering: {query}\nContext: {context}\nDocs: {docs}"

# --- Flexible assembly ---
agent = Agent(
    memory=Memory(),
    tools=ToolBox(),
    retriever=Retriever(index_name="faiss"),
)
agent.tools.register("web_search")
print(agent.run("What is DI?"))
```

**Key takeaway:** Inheritance creates tight coupling. Composition creates flexible, testable systems — essential when you're building AI agents from pluggable components.

---

## 🔴 10. Pydantic — Runtime Validation

**What:** A library that enforces type hints at *runtime* and provides smart parsing/serialization. The de facto standard for data validation in FastAPI and Gen AI apps.

**Why it matters for interviews:** "How do you validate user input in a Python API?" Pydantic is the answer. Also essential for LLM output parsing.

**Gen AI angle:** Pydantic is the backbone of LangChain, LlamaIndex, and any LLM output parsing pipeline.

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import list

class Document(BaseModel):
    """A retrieved document with metadata."""
    text: str
    source: str
    score: float = Field(ge=0.0, le=1.0)  # ge=greater-equal, le=less-equal
    tags: list[str] = Field(default_factory=list)

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty")
        return v

    model_config = ConfigDict(extra="forbid")  # Reject unknown fields

# --- Pydantic does runtime validation ---
doc = Document(text="Python is great", source="wiki", score=0.95)
print(doc)  # Auto-parsed, validated

# doc = Document(text="", source="x", score=1.5)
# → ValueError: text must not be empty; score must be <= 1.0

# --- Auto JSON serialization ---
json_str = doc.model_dump_json(indent=2)
loaded = Document.model_validate_json(json_str)  # Round-trip
```

**Interview must-know patterns:**
```python
# 1. Nested models
class Query(BaseModel):
    question: str
    documents: list[Document]

# 2. Union types for polymorphic input
from typing import Union
class SearchInput(BaseModel):
    query: str
    filter: Union[str, list[str], None] = None

# 3. ConfigDict for ORM-style integration
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Accept ORM objects
    name: str
    email: str
```

---

## 🔴 11. Structured LLM Output / Schemas

**What:** Getting LLMs to return data in a predictable, typed format (JSON, Pydantic models) instead of free-text. The backbone of reliable Gen AI systems.

**Why it matters for interviews:** Every Gen AI role asks about structured output. "How do you make an LLM return a specific JSON shape?" is a top interview question.

**Gen AI angle:** This is THE topic for Gen AI interviews. Tool calling, function calling, JSON mode — all are ways to get structured output.

```python
from pydantic import BaseModel, Field
from typing import Optional
import json

# --- Define the expected schema ---
class MovieReview(BaseModel):
    title: str
    rating: int = Field(ge=1, le=5)
    sentiment: str = Field(pattern="^(positive|negative|neutral)$")
    reasons: list[str] = Field(min_length=1)

class ReviewBatch(BaseModel):
    reviews: list[MovieReview]
    overall_sentiment: str

# --- Option 1: Prompt the LLM for JSON, then validate ---
# (In production, use the LLM's native JSON mode or tool calling)
raw_llm_response = '''
{
  "reviews": [
    {"title": "Inception", "rating": 5, "sentiment": "positive", "reasons": ["mind-bending"]},
    {"title": "Boring Movie", "rating": 2, "sentiment": "negative", "reasons": ["slow"]}
  ],
  "overall_sentiment": "mixed"
}
'''

# Parse + validate in one line
batch = ReviewBatch.model_validate_json(raw_llm_response)
print(batch.reviews[0].rating)  # 5
# batch = ReviewBatch.model_validate_json("not json")  # ← Validation error!

# --- Option 2: Pydantic + openai SDK (structured output) ---
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

client = OpenAI()

response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "Analyze these reviews"}],
    response_format=ReviewBatch,  # ← Pydantic model as schema!
)
parsed: ReviewBatch = response.data  # Guaranteed to match the schema
```

**Why this matters:** Without structured output, you're parsing fragile regexes off free text. With Pydantic + LLM JSON mode, you get compile-time type safety on LLM responses.

**Tool calling = structured output:**
```python
# Tool definitions ARE Pydantic-like schemas
class SearchTool(BaseModel):
    query: str
    max_results: int = 5

# The LLM calls this tool → arguments are validated automatically
# Equivalent to: response includes {name: "search", arguments: {"query": "...", "max_results": 5}}
```

---

## 🟡 12. `Callable` — Typing Functions

**What:** A way to type hint that a parameter expects a *callable* (function, lambda, method) with a specific signature.

**Why it matters for interviews:** Often used in callbacks, higher-order functions, and LLM tool definitions. Interviewers ask about `Callable[[int, str], bool]` syntax.

**Gen AI angle:** Callbacks for LLM callbacks (LangChain), tool functions, scoring functions.

```python
from typing import Callable

# Callable[[ArgTypes...], ReturnType]
# Callable[[int, str], bool] means: takes (int, str), returns bool

def process_data(
    data: list[int],
    transform: Callable[[int], float],
    filter_fn: Callable[[float], bool] = lambda x: x > 0,
) -> list[float]:
    results = [transform(x) for x in data]
    return [r for r in results if filter_fn(r)]

# Usage — any function matching the signature works
def square_to_float(x: int) -> float:
    return float(x ** 2)

def positive_only(x: float) -> bool:
    return x > 0

print(process_data([1, -2, 3], transform=square_to_float, filter_fn=positive_only))
# [1.0, 9.0]

# --- Gen AI: LLM scoring callback ---
def evaluate_response(
    response: str,
    judge: Callable[[str], float],  # Returns a 0–1 score
) -> float:
    return judge(response)

# Different judges, same interface
def llama_judge(text: str) -> float:
    return 0.85

def gpt_judge(text: str) -> float:
    return 0.92

score = evaluate_response("Great answer!", judge=gpt_judge)
```

**`ParamSpec` is the advanced cousin** (see topic 15) — it preserves the parameter types of the wrapped callable.

---

## 🟡 13. Generics / `TypeVar` — Reusable Type-Safe Components

**What:** `TypeVar` creates a *placeholder type* that gets filled in by the caller. Generics let you write functions/classes that work with *any* type while preserving type information.

**Why it matters for interviews:** The #1 advanced typing topic. "What is a TypeVar?" "What's the difference between `List[T]` and `list`?" "Why use Generic over Any?"

**Gen AI angle:** Generic repositories, vector stores, prompt templates — components that work across many types.

```python
from typing import TypeVar, Generic, list

T = TypeVar("T")  # A placeholder type

# Generic function — works for ANY type
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Type is PRESERVED at call site:
names: list[str] = ["Alice", "Bob"]
age = first([25, 30, 35])
print(first(names))  # → str | None, type checker knows it's str
print(age)           # → int | None

# --- Generic class ---
class VectorStore(Generic[T]):
    """A generic store that works for any embedding type."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def search(self, query: T, top_k: int = 5) -> list[T]:
        return self._items[:top_k]  # Simplified

# Create type-specific stores
string_store: VectorStore[str] = VectorStore(dimension=128)
string_store.add("hello")

# Embedding store — a list[float] is an embedding
from typing import TypeAlias
Embedding: TypeAlias = list[float]
vec_store: VectorStore[Embedding] = VectorStore(dimension=1536)
vec_store.add([0.1, 0.2, 0.3])
```

**`TypeVar` with bounds (interview favorite):**
```python
from typing import TypeVar, SupportsAbs

# T must be a subtype of SupportsAbs (has __abs__)
T = TypeVar("T", bound=SupportsAbs)

def abs_sum(items: list[T]) -> float:
    return sum(abs(item) for item in items)

abs_sum([1, -2, 3])      # OK — ints support abs()
abs_sum([1.5, -2.5, 3.5]) # OK — floats support abs()
# abs_sum(["a", "b"])   # ← Type error! str doesn't support abs()
```

---

## 🟡 14. `Literal` — Constrained Values

**What:** Restricts a variable to one of a specific set of literal values. Tells the type checker "this can ONLY be one of these values."

**Why it matters for interviews:** "What's the difference between `Literal` and `Enum`?" "When would you use Literal?" Common interview question about constrained types.

**Gen AI angle:** Model names, output formats, sampling strategies, API statuses — anything with a fixed set of valid values.

```python
from typing import Literal
from typing import Union

# Restrict to specific string values
ModelName = Literal["gpt-4o", "claude-3.5", "llama-3"]

def configure(model: ModelName, temperature: float = 0.7) -> None:
    print(f"Configuring {model} at temp={temperature}")

configure("gpt-4o")       # OK
configure("claude-3.5")   # OK
configure("gpt-3.5")      # ← Type error! Not in the Literal set
configure("unknown")      # ← Type error!

# Combine with Union for complex constraints
class Task(BaseModel):
    type: Literal["classification", "generation", "summarization"]
    model: ModelName
    config: dict[str, float]

# --- vs Enum ---
# Literal is lighter-weight; Enum is a full class
from enum import Enum

class OutputFormat(str, Enum):
    JSON = "json"
    TEXT = "text"
    MARKDOWN = "markdown"

# Prefer Literal when: you want str compatibility, minimal overhead
# Prefer Enum when: you need methods, iteration, or richer behavior

# --- Practical Gen AI usage ---
def stream_response(
    model: ModelName,
    stream_mode: Literal["text", "json", "tool"],
) -> str:
    """Stream mode determines how the LLM returns."""
    ...

stream_response("gpt-4o", "json")   # OK
stream_response("gpt-4o", "audio")  # ← Type error!
```

**Interview answer for Literal vs Enum:**
- `Literal` is a type hint — no runtime overhead, works with strings directly
- `Enum` is a full class — has methods, iteration, but requires `.value` access
- Use `Literal` for simple constrained strings; use `Enum` when you need richer behavior

---

## 🟡 15. `ParamSpec` — Preserving Callable Signatures

**What:** A `TypeVar` for *parameters*. It captures the full signature of a callable so that decorators can preserve type information.

**Why it matters for interviews:** "How do you type a decorator that preserves the wrapped function's signature?" This is the advanced answer. Without ParamSpec, decorators lose type info.

**Gen AI angle:** Wrapping LLM clients with logging, retries, caching — all need to preserve the original function signature.

```python
from typing import ParamSpec, Callable, TypeVar
from functools import wraps
import time

P = ParamSpec("P")  # Captures the *parameters* of a function
R = TypeVar("R")    # Captures the *return type*

# Without ParamSpec, a decorator loses signature info:
def timer(prefix: str) -> None:
    """Poor man's decorator — NO ParamSpec, loses types!"""
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> R:
            start = time.time()
            result = func(*args, **kwargs)
            print(f"{prefix}: {func.__name__} took {time.time()-start:.3f}s")
            return result
        return wrapper
    return decorator

# --- WITH ParamSpec — FULL type preservation ---
def logged_call(prefix: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Type-safe decorator preserving P (params) and R (return type)."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.time()
            result = func(*args, **kwargs)
            print(f"[{prefix}] {func.__name__} executed in {time.time()-start:.4f}s")
            return result
        return wrapper
    return decorator

# --- Now the decorated function keeps its signature! ---
@logged_call("[LLM]")
def generate_response(model: str, prompt: str, max_tokens: int = 100) -> str:
    return f"Generated by {model}: {prompt[:30]}..."

# Type checker KNOWS the signature after decoration:
result: str = generate_response("gpt-4o", "Hello", max_tokens=50)
# generate_response(123, 456)  # ← Type error! model must be str

# --- Real Gen AI usage: retry decorator ---
@logged_call("[RETRY]")
def llm_complete(client: OpenAIClient, prompt: str) -> str:
    return client.complete(prompt)
```

**Why ParamSpec matters:**
- Without it: `Callable[..., R]` — loses parameter names and types
- With it: `Callable[P, R]` — preserves full signature
- Combined with `Consecutive`, you can enforce parameter ordering

**The pattern to remember in interviews:**
```python
P = ParamSpec("P")
R = TypeVar("R")

def my_decorator(func: Callable[P, R]) -> Callable[P, R]:
    ...  # Preserve both params and return type
```

---

## Quick Reference: When to Use What

| Topic | Use When... | Gen AI Example |
|---|---|---|
| `TypedDict` | JSON-like dicts with fixed keys | LLM response schemas |
| `dataclass` | Pure data containers with defaults | Model configs, dataset records |
| `Protocol` | Structural interfaces (duck typing) | Swap LLM providers |
| `ABC` | Enforced runtime interfaces | Plugin architectures |
| `DI` | Swappable dependencies | Mock LLM clients for tests |
| `Composition` | Complex objects from simple parts | Agent = Memory + Tools + Retriever |
| `Pydantic` | Runtime validation + parsing | Request validation, LLM output parsing |
| `Structured LLM` | Predictable LLM responses | JSON mode, tool calling |
| `Callable` | Typing functions as arguments | LLM scoring callbacks |
| `Generics/TypeVar` | Reusable type-safe components | Generic vector stores |
| `Literal` | Fixed set of string values | Model names, output formats |
| `ParamSpec` | Type-preserving decorators | Retry/logging wrappers for LLM clients |

### Exercises

1. Add complete annotations to a small untyped module and run mypy or pyright.
2. Define a `TypedDict` for an API response with one optional field.
3. Define a protocol for a cache with `get` and `set`, then implement in-memory and fake versions.
4. Write generic `last(items)` while handling the empty sequence explicitly.
5. Replace unnecessary `Any` annotations in an example with more precise types.

---

## 9. Concurrency: threads, processes, and asyncio

### Choose by workload

| Model | Best fit | Main cost/risk |
|---|---|---|
| `asyncio` | Many concurrent I/O operations using async libraries | Blocking the event loop; cancellation complexity |
| Threads | Blocking I/O or synchronous libraries | Races, locks, thread overhead, GIL limits CPU-bound Python |
| Processes | CPU-bound Python work across cores | Startup, memory, serialization, inter-process communication |

The practical interview answer is not "async is faster." It is "choose based on whether work is waiting on I/O or consuming CPU, and based on the libraries already in use."

### The GIL at interview depth

In the normal CPython build, the Global Interpreter Lock allows only one thread at a time to execute Python bytecode within a process. Threads can still help I/O-bound workloads because a waiting operation can release execution to another thread. Processes are the usual answer for parallel CPU-bound pure-Python work.

Do not claim that the GIL makes threads useless or that every operation is automatically thread-safe.

### Basic asyncio

```python
import asyncio


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"finished {name}"


async def main() -> None:
    results = await asyncio.gather(
        fetch("a", 0.2),
        fetch("b", 0.1),
    )
    print(results)


asyncio.run(main())
```

Calling an `async def` function creates a coroutine object. It does not run to completion until awaited or scheduled.

### Tasks and structured concurrency

```python
import asyncio


async def main() -> None:
    async with asyncio.TaskGroup() as group:
        first = group.create_task(fetch("a", 0.2))
        second = group.create_task(fetch("b", 0.1))

    print(first.result(), second.result())
```

`TaskGroup` gives related tasks a clear lifetime and coordinated failure handling.

### Limit concurrency

Unbounded concurrency can overload a downstream service or exhaust connections.

```python
import asyncio

semaphore = asyncio.Semaphore(10)


async def limited_fetch(item: str) -> str:
    async with semaphore:
        return await fetch(item, 0.1)
```

### Cancellation and blocking work

Do not swallow `asyncio.CancelledError` accidentally. Use `try/finally` for cleanup. Never call blocking `time.sleep()` inside async code; use `await asyncio.sleep()`.

Move a small blocking I/O call to a thread with `await asyncio.to_thread(function, *args)`. For sustained CPU work, consider a process pool or an external worker.

### Race conditions

A race occurs when correctness depends on timing between concurrent operations. Protect shared mutable state with the appropriate lock, or redesign to avoid sharing it.

### Likely interview questions

- Thread versus process versus coroutine?
- What is the GIL, and what does it not mean?
- What happens when an async function is called without `await`?
- `asyncio.gather` versus `TaskGroup`?
- How do you limit concurrent requests?
- Why is `time.sleep()` harmful in async code?
- How do timeout, cancellation, and cleanup interact?

### Exercises

1. Run three simulated I/O calls sequentially, then concurrently; measure elapsed time.
2. Add a semaphore so only five calls run simultaneously.
3. Add a timeout and verify resources are cleaned up after cancellation.
4. Introduce a race in a shared counter, then fix it with a lock.
5. Classify five workloads as async, threaded, or process-based and defend each answer.
6. Write the same URL-fetching task with a thread pool and asyncio; compare operational trade-offs.

---

## 10. Testing, mocking, and debugging

### Test behavior, not implementation details

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

### Fixtures

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

### Parametrization

```python
@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1", 1), ("20", 20), ("-3", -3)],
)
def test_parse_integer(raw: str, expected: int) -> None:
    assert int(raw) == expected
```

### Mock at a boundary

Mock network, clock, filesystem, or database boundaries when a unit test should not use the real dependency. Patch the name where the code under test looks it up, not necessarily where it was originally defined.

Prefer a small fake implementing a protocol when extensive mocking starts to mirror implementation details.

### Async tests

With `pytest-asyncio`:

```python
import pytest


@pytest.mark.asyncio
async def test_fetch() -> None:
    result = await fetch("item", 0)
    assert result == "finished item"
```

### Debugging approach

1. Reproduce the issue reliably.
2. Reduce it to the smallest failing input.
3. Read the complete traceback from the bottom upward.
4. Inspect assumptions using a debugger, structured logs, or temporary assertions.
5. Fix the cause and add a regression test.

Know `breakpoint()`, traceback reading, logging levels, and the difference between a unit test and an integration test.

### Likely interview questions

- What makes a good unit test?
- Fixture versus helper function?
- Mock versus fake?
- Where should `patch` be applied?
- How do you test exceptions and async functions?
- Unit, integration, and end-to-end tests: what does each prove?
- How would you debug an intermittent production failure?

### Exercises

1. Test the happy path, invalid input, and dependency failure for one service function.
2. Parametrize ten edge cases for a parser.
3. Replace a network client with a protocol-based fake.
4. Test retry behavior without actually waiting by patching the sleep boundary.
5. Debug a failing function using `breakpoint()` and write a regression test.

---

## 11. Coding problems and complexity

### What interviewers assess

They are usually evaluating more than the final answer:

- Did you clarify inputs and edge cases?
- Did you choose the right collection?
- Is the solution correct and readable?
- Can you state time and space complexity?
- Can you improve a brute-force solution?
- Can you test your own code with examples?

### A reliable interview method

1. Restate the problem and ask about constraints.
2. Give one small example, including an edge case.
3. Explain a straightforward approach.
4. Improve it if the constraints require it.
5. Write readable code with meaningful names.
6. Dry-run the code aloud.
7. State time and space complexity.

### Essential patterns

#### Frequency map

```python
from collections import Counter


def first_unique(text: str) -> str | None:
    counts = Counter(text)
    return next((character for character in text if counts[character] == 1), None)
```

#### Set for seen values

```python
def has_duplicate(values: list[int]) -> bool:
    seen: set[int] = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False
```

#### Two pointers

Useful for sorted arrays, palindrome checks, and in-place partitioning.

#### Sliding window

Useful for contiguous subarrays/substrings, especially longest/shortest windows satisfying a condition.

#### Stack and queue

Use a list as a stack with `append`/`pop`. Use `deque` as a queue with `append`/`popleft`.

#### Heap

Use `heapq` for top-k, scheduling, and repeatedly retrieving the smallest item.

### Complexity worth memorizing

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

### Core exercise set

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

# GOOD TO KNOW

## 12. Files, JSON, serialization, and parsing

### Files

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

### JSON

```python
import json

payload = '{"id": 42, "active": true}'
data = json.loads(payload)
encoded = json.dumps(data, indent=2, sort_keys=True)
```

Know the distinction: `loads` parses a `str`, `bytes`, or `bytearray`; `dumps` always returns a `str`. `load` reads from a file-like object, while `dump` writes text to one.

Validate external data before relying on its fields and types.

### Pickle safety

`pickle` preserves Python-specific object structures, but loading a pickle can execute arbitrary code. Never unpickle untrusted or unauthenticated data.

### Parsing

Prefer a real parser or structured API for structured formats. Avoid fragile string splitting when CSV, JSON, URL, date/time, or shell syntax has a standard parser.

### Likely interview questions

- Why use `with open(...)`?
- `read`, `readline`, and iteration over a file?
- `json.load` versus `json.loads`?
- Why is pickle unsafe for untrusted data?
- How would you process a 20 GB log file?

### Exercises

1. Stream a large JSON Lines file and report invalid rows without stopping the entire job.
2. Merge two configuration files with explicit override precedence.
3. Parse CSV with quoted commas using the `csv` module rather than `split(",")`.
4. Write results atomically using a temporary file followed by replacement.
5. Design a serializer for a dataclass containing a `datetime` and explain the format choice.

---

## 13. Memory management and performance

### References and garbage collection

CPython primarily uses reference counting: an object's reference count changes as references are created or removed, and an object can usually be reclaimed when the count reaches zero. A cyclic garbage collector handles unreachable reference cycles.

This is an implementation-level explanation, not a guarantee for every Python interpreter. Do not build normal application logic around an exact destruction time; use context managers for deterministic resource cleanup.

### Measure before optimizing

Use the right tool for the question:

- `timeit` for small timing comparisons
- `cProfile` for function-level CPU profiling
- `tracemalloc` for Python memory allocation tracing
- application metrics and tracing for production bottlenecks

### Common practical improvements

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

### Likely interview questions

- How does Python manage memory at a high level?
- What are reference cycles?
- How would you investigate a memory increase?
- Generator versus list memory usage?
- How do you profile slow Python code?
- Why is algorithm choice often more important than micro-optimization?

### Exercises

1. Use `timeit` to compare list and set membership at different sizes.
2. Use `tracemalloc` to compare a materialized pipeline with a generator pipeline.
3. Profile a deliberately slow text-processing function and improve the measured bottleneck.
4. Find and remove repeated O(n) work inside a loop.
5. Explain why `sys.getsizeof(container)` does not necessarily include all nested objects.

---

## 14. Environments and packaging

### Package basics

- A package groups modules, commonly in a directory.
- `__init__.py` commonly marks and initializes a regular package, although namespace packages can exist without it.
- Prefer clear absolute imports in application code, such as `from project.services.users import UserService`.

### Virtual environments and project metadata

A virtual environment provides an isolated package installation location and command environment while normally sharing the base Python installation and standard library.

Modern projects commonly define metadata and dependencies in `pyproject.toml`. Tools such as `pip`, `uv`, or Poetry can install/manage dependencies; understand the tool used by the target company rather than trying to master every tool.

Know the purpose of:

- direct dependencies versus transitive dependencies
- version constraints and lock files
- editable installs during development
- reproducible environments

### Likely interview questions

- Why use a virtual environment?
- What belongs in `pyproject.toml`?
- Direct dependency versus transitive dependency?
- What is the purpose of a lock file?

### Exercises

1. Turn two related modules into a small package with clear absolute imports.
2. Add a `pyproject.toml` and install the package in editable mode.
3. Create a fresh virtual environment and prove that its installed packages differ from another environment.
4. Write a CLI entry point that does no expensive work during import.
5. Explain how you would pin dependencies for an application versus declare compatible ranges for a library.

---

## 15. Useful standard-library tools

You do not need to memorize the whole standard library. Recognize these tools and know the problem each solves.

### `functools`

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

### `itertools`

- `chain`: iterate over multiple iterables as one
- `islice`: slice an iterator lazily
- `groupby`: group adjacent items sharing a key
- `product`: Cartesian product
- `combinations`: combinations without replacement

`groupby` groups consecutive items with the same key. Sort first only when all items sharing a key must form one group; sorting may destroy meaningful input order.

### `collections`

- `Counter`: frequencies
- `defaultdict`: default values for missing keys
- `deque`: efficient work at both ends
- `OrderedDict`: explicit ordering operations; still useful for LRU-style behavior
- `ChainMap`: layered mappings

### Other useful modules

- `heapq`: min-heap/top-k problems
- `bisect`: binary search/insertion in a sorted list
- `pathlib`: filesystem paths
- `datetime` and `zoneinfo`: time and time zones
- `enum`: named finite choices
- `contextlib`: context-manager helpers

### Likely interview questions

- How would you implement memoization?
- How does `groupby` handle consecutive keys, and when should input be sorted first?
- Efficient top-k elements?
- `deque` versus list for a queue?
- Why prefer timezone-aware datetimes?

### Exercises

1. Build an LRU cache with `OrderedDict`, then compare it with `functools.lru_cache`.
2. Return the top five events using `heapq` without sorting the entire input.
3. Lazily combine and batch several iterables using `chain` and `islice`.
4. Group sorted records with `itertools.groupby`, then demonstrate the result with unsorted input.
5. Convert an aware timestamp between two zones using `zoneinfo`.

---

# Practice Resources

## YouTube learning links

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

## Python coding-practice links

### Best starting choices

- [HackerRank Python domain](https://www.hackerrank.com/domains/python): topic-based drills for collections, exceptions, classes, decorators, and language syntax.
- [Exercism Python track](https://exercism.org/tracks/python/exercises): test-driven exercises with community solutions and optional mentoring.
- [Practice Python](https://www.practicepython.org/): short beginner-to-intermediate exercises; useful for quick daily repetitions.

### Interview problem practice

- [LeetCode problem set](https://leetcode.com/problemset/): use Python and focus first on arrays, strings, hash tables, stacks, queues, heaps, and sliding windows.
- [HackerRank interview preparation kit](https://www.hackerrank.com/interview/interview-preparation-kit): structured algorithm practice.
- [Codewars Python](https://www.codewars.com/kata/search/python): short kata with many community solutions; compare solutions only after submitting yours.

### Topic exercises with solutions

- [PYnative Python exercises](https://pynative.com/python-exercises-with-solutions/): exercises grouped by topic, with solutions for checking after attempting.
- [Exercism Python repository](https://github.com/exercism/python): exercise instructions and tests that can be run locally.
- [Corey Schafer code snippets](https://github.com/CoreyMSchafer/code_snippets): source code accompanying many of the linked videos.

### Official references

- [Python tutorial](https://docs.python.org/3/tutorial/)
- [Python standard library](https://docs.python.org/3/library/)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [pytest documentation](https://docs.pytest.org/)

### Recommended practice mapping

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

## Final mock-round checklist

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

### A realistic readiness test

Run a 60-minute mock round:

1. 15 minutes: answer five concept questions from Sections 1-8.
2. 25 minutes: solve one easy-to-medium coding problem and test it.
3. 10 minutes: answer one concurrency scenario.
4. 10 minutes: review a short function for correctness, readability, typing, and test gaps.

You are ready when your explanations are clear and your code is correct and readable. Perfect recall of obscure Python internals is not required.
