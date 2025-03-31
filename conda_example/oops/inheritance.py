from re import U


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age 
    def getDetails(self):
        return f"Name: {self.name}, Age: {self.age}"
    
class Employee(User):
    def __init__(self, name, age, emp_id):
        super().__init__(name, age) 
        self.emp_id = emp_id

    def getDetails(self):
        return f"${super().getDetails()}, Emp ID: {self.emp_id}"

emp = Employee('EmpA', 25, 123)
print(emp.getDetails())