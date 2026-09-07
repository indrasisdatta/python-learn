"""
*args / **kwargs in function definition -> Collect 
*list / **dict in function call -> unpack
"""

# Function definition 
def logger(event, *args, **kwargs):
    print(f"Event: {event}")
    print(args)
    print(kwargs)


logger(
    "Add to cart",
    '/cart',
    'prod001',
    userId=12,
    correlationId="corr9968768"
)


# Function call 
def add(a, b, c):
    return a + b + c 

nums = [3, 5, 10]
print(add(*nums))

