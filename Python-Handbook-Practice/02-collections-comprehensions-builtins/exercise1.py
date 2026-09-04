# Remove duplicates from a list while preserving first-seen order.

nums = [100, 5, 50, 2, 20, 1, 5, 100]

# NOTE: Set does not guarantee insertion order
# This won't maintain the insertion order
# print(list(set(nums)))

# Approach 1: Using set
# unique = set()
result = []

for num in nums:
    if num not in result:
        # unique.add(num)
        result.append(num)

print(result)

# Approach 2: Using dict (dict maintains insertion order)
print(list(dict.fromkeys(nums)))