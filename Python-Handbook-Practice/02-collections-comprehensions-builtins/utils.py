"""
1. enumerate(items) for index-value pairs
2. zip(a, b) for parallel iteration
3. sorted(items, key=..., reverse=...) for a new sorted list
4. min, max, and sum
5. any and all
6. map and filter (and when a comprehension is clearer)
"""

# ------- 1. enumerate(items) for index-value pairs -------
# ----------------------------------------------------------
# enumerate - returns enumerate object (an itertaor)
# An iterator is both an iterable and an iterator 
# List is iterable but not an iterator 

countries = ["India", "Australia", "UK"]
for i, val in enumerate(countries):
    print(i, val)

e = enumerate(countries)
print(iter(e) is e)


# ------- 2. zip(a, b) for parallel iteration --------------
# ----------------------------------------------------------

capitals = ["New Delhi", "Canberra", "London"]
# zipped = zip(countries, capitals)
# print(next(zipped))
# print(iter(zipped) is zipped)
result = { country: capital for country, capital in zip(countries, capitals) }
print(result)

print(sorted([12, 0, -2, 45, 1000], reverse=True))

# ------- 3. sorted(items, key=..., reverse=...) for a new sorted list -----
# --------------------------------------------------------------------------

users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 22},
    {"name": "Charlie", "age": 25}
]

# Standard function
def get_age(user):
    return user['age']
ageDesc = sorted(users, key=get_age, reverse=True)
print(ageDesc)

# Lambda
ageAsc = sorted(users, key = lambda user: user['age'])
print(ageAsc)

print(users)

# ------- 4. min, max, and sum -----------------------------
# ----------------------------------------------------------

print(min([12,45,-1,476]))
print(sum([5, 4, 10, 1], 5))

print(min(users, key=lambda user: user['age']))

# ------- 5. any and all ----------------------------------
# ----------------------------------------------------------

any([]) # False
all([]) # True - can't find any falsy, so defaults to True

print(
    any(
        [user['age'] > 30 for user in users]
    )
)
print(
    all(
        [user['age'] > 18 for user in users]
    )
)


# ----- 6. map and filter (and when a comprehension is clearer) ------
# --------------------------------------------------------------------
filtered = filter(lambda user: user['age'] > 25, users)
print(list(filtered))

# list.sort() sorts the list in-place and returns None. 
# sorted() creates a new sorted list and leaves the original unchanged. 

# sorted() also works with any iterable, whereas .sort() is a list method.