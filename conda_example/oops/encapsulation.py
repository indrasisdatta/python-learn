class User:
    def __init__(self, name, age, gender):
        self.__name = name # Private variable
        self._age = age   # Protected variable
        self.gender = gender
    def getDetails(self):
        return f"Name: {self.__name}, Age: {self._age}, Gender: {self.gender}"

user = User('UserA', 20, 'Male')
dir(user)
print(user.getDetails())