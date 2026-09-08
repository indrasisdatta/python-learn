"""
Create a custom RangeLike iterator without using range internally.
"""

class RangeLike:
    start: int 
    end: int 

    def __init__(self, start, end):
        self.start = start 
        self.end = end 

    def __iter__(self):
        return self

    def __next__(self):
        if (self.start > self.end):
            raise StopIteration("Limit reached")

        value = self.start
        self.start += 1
        return value
            

my_range = RangeLike(5, 10)
print(next(my_range))
print(next(my_range))
print(next(my_range))
print(next(my_range))
print(next(my_range))
print(next(my_range))