from abc import ABC, abstractmethod

# Abstract base class
class Bank(ABC):
    @abstractmethod
    def withdraw(self):
        pass 

    @abstractmethod
    def deposit(self):
        pass 

    def check_balance(self):
        return "Your balance is: $"

class Savings(Bank):
    def __init__(self, amount):
        self.amount = amount
    def withdraw(self, amount):
        if (self.amount > 0):
            self.amount -= amount
    def deposit(self, amount):
        self.amount += amount   

    def check_balance(self):
        return f"{super().check_balance()} {self.amount}"

sbiAcc = Savings(500)
sbiAcc.deposit(100)
sbiAcc.deposit(100)
sbiAcc.deposit(100)
sbiAcc.withdraw(600)

print(sbiAcc.check_balance())
