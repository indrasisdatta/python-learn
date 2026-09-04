class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age 

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.name == other.name and self.age == other.age 

user1 = User("John", 12)
user2 = User("John", 12)
print(user1 == user2)
print(user1 is user2)