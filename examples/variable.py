num1 = 25
num2 = 25.75

# print(type(num1))
# print(type(num2))
# print(float(num1))

import random
# Random integer value from 0 to 9
print(random.randint(0, 9))

# Prints 0.30000000000000004 instead of 0.3
print(0.1 + 0.1 + 0.1)
# handle decimal precision
from decimal import Decimal
print(Decimal('0.1')+Decimal('0.1')+Decimal('0.1'))