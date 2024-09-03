# Find the first non-repeated character
str = 'An Apple'
charCount = {}
for i in str:
    # In-build function to check char count
    # print(i, str.count(i))
    if i == ' ': 
        continue
    if (i in charCount):
        charCount[i] =  charCount[i] + 1
    else:
       charCount[i] = 1
print('Frequency of characters', charCount)

for chr, count in charCount.items():
    if count == 1:
        print('First non-repeating character: ', chr)
        break;
