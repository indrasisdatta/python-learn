import math
# from operator import mul

def result(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius 
    return round(area, 2), round(circumference, 2)

area, circum = result(3)

# print('Area: ', area, 'Circumference: ', circum);

def multiplyAll(*args):
    # Debug code
    # print(args, type(args));
    # Custom multiply code
    result = 1
    for num in args:
        result *= num
    return result

print(multiplyAll(1, 2, 3, 4, 5));