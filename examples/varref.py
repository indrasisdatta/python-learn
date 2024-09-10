myListOne = [1, 2, 3]
myListTwo = myListOne;
# myListOne = [4, 5] // changes only this var
# myListOne = 'test' // changes only this var
# changes both vars
myListOne[0] = 100; 
print(myListOne)
print(myListTwo)

h1 = [1, 2, 3]
# Copy of h1
h2 = h1[:]
h1[0] = 100
print(h1)
print(h2)

list1 = [20, 30, 40]
list2 = list1;
# Check ref
print(list1 is list2)
# Check value
print(list1 == list2)