myList = [0, 1, 2, 3, 4]
# Insert 100, 200 at 1 and 2 pos
myList[1:1] = [100, 200]
print(myList)
# Remove elements from 1, 2 pos
myList[1:3] = []
print(myList)

myList.append(500)
if (500 in myList):
    print('500 exists')

myListCopy = myList.copy()

# Insert at pos 1
myList.insert(1, 111)
print(myList)
print(myListCopy)

# Find square of nos 1 to 4 (1, 4, 9, 16)
squaredNum = [x**2 for x in range(1, 5)]
print(squaredNum)