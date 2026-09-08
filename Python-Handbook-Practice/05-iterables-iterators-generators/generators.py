"""
Compare the approximate memory used by a list comprehension and generator expression 
for one million integers.

"""
import sys

list = [x for x in range(1, 1_000_000)]
gen = (x for x in range(1, 1_000_000))

print(f"{type(list)} - memory {sys.getsizeof(list)}")
print(f"{type(gen)} - memory {sys.getsizeof(gen)}")