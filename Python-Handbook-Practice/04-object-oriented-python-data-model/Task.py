"""
Build a Task dataclass with id, priority, and created_at, then sort tasks.
priority DESC created_at ASC
"""

from dataclasses import dataclass 

@dataclass
class Task: 
    id: int   
    priority: int 
    created_at: str
     

tasks = [
    Task(1, 4, "2026-04-12"),
    Task(2, 1, "2026-04-12"),
    Task(3, 1, "2026-04-10"),
    Task(4, 3, "2026-06-05"),
    Task(5, 2, "2026-06-01")
]

sorted_tasks = sorted(
    tasks,
    key=lambda task: (-task.priority, task.created_at)
)

print(sorted_tasks)