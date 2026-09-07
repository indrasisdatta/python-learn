# Sort API records by descending priority, then ascending creation time
api_records = [
    {"id": 1, "priority": 3, "created_at": "2024-01-15T10:30:00", "endpoint": "/users"},
    {"id": 2, "priority": 1, "created_at": "2024-01-10T08:00:00", "endpoint": "/orders"},
    {"id": 3, "priority": 2, "created_at": "2024-01-12T14:20:00", "endpoint": "/products"},
    {"id": 4, "priority": 3, "created_at": "2024-01-10T09:15:00", "endpoint": "/auth"},
    {"id": 5, "priority": 1, "created_at": "2024-01-14T16:45:00", "endpoint": "/payments"},
    {"id": 6, "priority": 2, "created_at": "2024-01-10T11:00:00", "endpoint": "/inventory"},
    {"id": 7, "priority": 3, "created_at": "2024-01-11T07:30:00", "endpoint": "/notifications"},
    {"id": 8, "priority": 2, "created_at": "2024-01-13T12:00:00", "endpoint": "/reports"},
]

# ISSUE: second sort can rearrange regarless of priority
# desc = sorted(api_records, key=lambda rec: rec['priority'], reverse=True)
# asc = sorted(desc, key=lambda rec: rec['created_at'])

result = sorted(api_records, key=lambda rec: (-rec['priority'], rec['created_at']))
print(result)