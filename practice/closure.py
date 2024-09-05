def operation(num):
    def calculate(pow):
        return num ** pow 
    return calculate 

square = operation(5)
print(square(2))

cube = operation(5)
print(cube(3))