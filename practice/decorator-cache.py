def cache(func):
    cache = {}
    def wrapper(*args):
        print(f"Calling function {func.__name__}", args)
        if (args in cache):
            print('Cache hit!')
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result 
    return wrapper 

@cache
def calculate(a, b, c):
    return a * b * c

print(calculate(4, 2, 3))
print(calculate(1, 2, 3))
print(calculate(4, 2, 3))
print(calculate(4, 2, 3))

#  py -m pip list