def add_event(event: str, events: list[str] | None = None) -> list[str]:
    if events is None:
        events = []
    events.append(event)
    return events

event1 = add_event("Event 1")
print(event1)

event2 = add_event("Event 2")
print(event2)

event3 = print(add_event("Event 3"))
print(event3)

# Incorrect - mutable
grid = [[0] * 3] * 3

# Correct approach
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)
print(grid[0] is grid[1])
