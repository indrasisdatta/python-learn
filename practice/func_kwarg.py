def print_kwargs(**kwargs):
    print(kwargs, type(kwargs))

print_kwargs(id=1, name="User A")
print_kwargs(id=2, name="User B", age=20)
print_kwargs(id=3)
