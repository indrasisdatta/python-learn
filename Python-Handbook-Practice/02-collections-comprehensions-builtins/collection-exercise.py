# Group a list of employees by department with defaultdict.

employees = [
    {"name": "Alice", "department": "Engineering"},
    {"name": "Bob", "department": "Marketing"},
    {"name": "Charlie", "department": "Engineering"},
    {"name": "Diana", "department": "Marketing"},
    {"name": "Eve", "department": "Engineering"},
    {"name": "Frank", "department": "HR"},
    {"name": "Grace", "department": "HR"},
    {"name": "Hank", "department": "Marketing"},
]

"""
Expected output:
{
    'Engineering': ['Alice', 'Charlie', 'Eve'],
    'Marketing': ['Bob', 'Diana', 'Hank'],
    'HR': ['Frank', 'Grace']
}
"""

# Normal dict - handle the missing check manually
grouped = {}
for emp in employees:
    if emp['department'] not in grouped:
        grouped[emp['department']]  = [] 
    grouped[emp['department']].append(emp['name'])

print(grouped)



# Using defaultdict - when a key is missing, create an empty list
from collections import defaultdict 

grouped = defaultdict(list)
for emp in employees: 
    grouped[emp['department']].append(emp['name'])

print(dict(grouped))
