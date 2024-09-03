items = ["banana", "apple", "banana", "orange", "apple", "mango"]
itemCount = {}

for str in items:
    if str in itemCount:
        print('Duplicate value: ', str)
        break;
    else:
        itemCount[str] = 1