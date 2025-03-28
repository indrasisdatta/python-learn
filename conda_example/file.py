import os

items = os.listdir('.');
print(items)

full_working_dir = os.path.join(os.getcwd(), 'example.csv')
print(f"Full working dir: {full_working_dir}")

abs_path = os.path.abspath('example.csv')
print(f"Abs path: {abs_path}")

print(f"Does path exist: {os.path.exists('example.csv')}")
print(f"Is dir: {os.path.isdir('example.csv')}")
print(f"Is file: {os.path.isfile('example.csv')}")