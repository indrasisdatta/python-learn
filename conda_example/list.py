str = "Hello"
for index, num in enumerate(str):
    print(f"{index}, {num}")

# Square of all nos from 1 to 5
square = [x**2 for  x in range(1,5)]
print(square)

# Square of even nos between 1 to 10
evenSquares = [x**2 for x in range(1, 10) if x % 2 == 0]
print(evenSquares)

# Nested list comprehension
dep_ids = ['001', '002', '003']
emp_names = ["John", "Mary", "Rob"]
pair = [[dep_id, emp_name] for dep_id in dep_ids for emp_name in emp_names]
print(pair)

# Feedback - find the no. of positive feedbacks 
feedbacks = ["Great service", "Excellent ambience", "Not happy", "Average", "Nice"]
positive_feedback_count = sum(1 for feed in feedbacks if "great" in feed.lower() or "excellent" in feed.lower() or "nice" in feed.lower())
print(f"Total positive feedbacks: {positive_feedback_count}")