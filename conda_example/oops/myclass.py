class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age 
    def getDetails(self):
        return f"Name: {self.name}, Age: {self.age}"

user = User('UserA', 20)
print(user.getDetails())