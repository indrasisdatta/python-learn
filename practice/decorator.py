def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}", args,kwargs )
        return func(*args, **kwargs)
    return wrapper

@debug
def greet(name, greet='Hello'):
    print(f"{greet} {name}")

greet('Indrasis', greet='Hi')