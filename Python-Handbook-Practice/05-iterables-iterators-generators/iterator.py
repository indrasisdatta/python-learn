"""
A list is iterable but not itself an iterator 
A generator object is both an iterator and an iterable 
An iterable prduces an iterator - when you call iter() on it 
An iterator produces values one at a time and maintains the iteration state 
Iterator is an object that implements __iter__() and __next__()
Iterable -> iter() -> Iterator -> next() -> values 
No more values - it throws StopIteration exception

Generator is one type of iterator (Lazy evaluation)
Produces one at a time when next() is called instead of creating lots of numbers in memory
"""

nums = iter([10,20])
try:
    print(next(nums))
    print(next(nums))
    print(next(nums))
except StopIteration:
    print(f"Exception ")


