students={
    "student1":{"name": "John", "age": 12, "std": "VI"},
    "student2":{"name": "Jane", "age": 13, "std": "VII"}
}
for std_key, std_val in students.items():
    print(f"------- {std_key} ------")
    for k,v in std_val.items():
        print(f"{k}: {v}")

# Dictionary comprehension

# Square of even nos
evens = { x: x**2 for x in (range(5)) if (x % 2 == 0)}
print(evens)

# Merge 2 dict into one
dict1 = { "a": 2, "b": 3 }
dict2 = { "c": 5, "d": 8, "a": 12 }
print({**dict1, **dict2})
