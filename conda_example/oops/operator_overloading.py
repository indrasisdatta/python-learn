class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real 
        self.imaginary = imaginary
    
    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary) 
    
    # def __str__(self):
    #     return f"{self.real} {self.imaginary}i"

    def __repr__(self):
        return f"{self.real} + {self.imaginary}i"
    
num1 = ComplexNumber(3, 5);
num2 = ComplexNumber(2, 3);
print(num1 + num2)
