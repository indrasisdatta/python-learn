scores = { "Adam": 50, "Jane": 34, "Jill": 42, "Spencer": 75 }

# Filter out passed dict
passed = {name: marks for (name, marks) in scores.items() if marks > 40}
print(passed)

# Dictionary merging
user = { "Adam": 50, "Jane": 34}
additional = { "Adam": 56 }
print(user | additional)