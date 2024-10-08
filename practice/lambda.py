def wrapper(n):
	return lambda a : a * n
    
double = wrapper(2)
triple = wrapper(3)

print(double(4))
print(triple(5))

