# Asynchronous Python — Interview Notes (Gen AI Lead / Architect)

> Target: CPython 3.11+ (with notes on 3.12 and the 3.14 free-threaded build).
> Emphasis on **architectural decision-making**, **failure handling**, and
> **observability** rather than toy "hello async" demos.

---

## Concurrency Model — Foundations

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
