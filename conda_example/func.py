# Positional arguments
def print_data(*args):
    print(args)
print_data(1, 2, 3, "Python script");

# Keyword arguments
def print_keyword(**kwargs):
    for key, val in kwargs.items():
        print(f"{key}: {val}")
print_keyword(id=1, name="Test")
