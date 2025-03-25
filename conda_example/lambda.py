# Map function
numbers = [1, 2, 5, 8, 12]
result = map(lambda x: x**2, numbers)
print(list(result))

# Filter function
persons = [
    {"name": "User A", "age": 20},
    {"name": "User B", "age": 13},
    {"name": "User C", "age": 16},
    {"name": "User D", "age": 33},
    {"name": "User E", "age": 32}
]
adults = filter(lambda p: p['age'] > 18, persons)
print(list(adults))