# Date time library
from datetime import datetime, timedelta
now = datetime.now()
yesterday = now - timedelta(days = 1)
print(now.strftime('%d %B, %Y'))
print(yesterday.strftime('%d %B, %Y'))

# Regular expression 
import re 
pattern = '\d+'
match = re.search(pattern, 'There are 10 items')
print(match.group())

# CSV operations 
import csv 

with open('example.csv', mode='w', newline='') as file: 
    writer = csv.writer(file)
    writer.writerow(['name', 'age'])
    writer.writerow(['User A', 21])
    writer.writerow(['User B', 31])
    writer.writerow(['User C', 24])


