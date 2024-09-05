def evenNosGenerator(limit):
    for i in range(1, limit+1, 2):
        yield i 

gen = evenNosGenerator(5)
print(type(gen))
try:
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
except StopIteration:
    print('End')


