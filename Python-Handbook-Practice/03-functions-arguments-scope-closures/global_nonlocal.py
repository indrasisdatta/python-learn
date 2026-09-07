"""
global - modify a variable at module level 
nonlocal - modify a variable in an enclosing function
"""

# Global example
a = 10
b = 5
def increment():
    global a 
    a += 1 

increment()
increment()
increment()
print(a)

# nonlocal example

def decrement():
    num = 10

    def calculate():
        nonlocal num
        num -= 1 
        return num
    
    return calculate

dec = decrement() 
print(dec())
print(dec())
print(dec())
