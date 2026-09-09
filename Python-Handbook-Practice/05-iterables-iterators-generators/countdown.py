"""
Write countdown(start) as a generator.
"""
def countdown(start):
    while start > 0:        
        yield start 
        start = start - 1

timer = countdown(5)
print(next(timer))
print(next(timer))
print(next(timer))
print(next(timer))
print(next(timer))
