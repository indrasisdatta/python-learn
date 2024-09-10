inputStr = '01234567'
print(inputStr[:-2])
print(inputStr[2:6])
# From 1 to 5, hop 2
print(inputStr[1:6:2])

str = "Hello, how are you?"
print(str.find('how'))
# Not found, so returns -1
print(str.find('hello'))
# find count
print(str.count('e'));

# Convert list to string - print using placeholder
fruitsStr = "apples, oranges, grapes, banana"
msg = "You've ordered {} fruits: {}"
fruitsList = fruitsStr.split(', ')
print(msg.format(len(fruitsList), fruitsList))

# List to string
myList = ['one', 'two', 'three']
print('-'.join(myList))