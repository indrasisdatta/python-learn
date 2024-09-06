class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model 
    def displayName(self):
        return f"{self.brand} {self.model}"
    
class ElectricCar(Car):
    def __init__(self, brand, model, batterySize):
        super().__init__(brand, model)
        self.__batterySize = batterySize
    def get_power(self):
        return self.__power
    def set_power(self, power):
        self.__power = power

    @staticmethod
    def sampleStaticMethod():
        return "This is a static method"
    
    # Used for read-only
    @property 
    def batterySize(self):
        return self.__batterySize
    
myCar = Car('Tata', 'Safari')
print(myCar.displayName())

myElectricCar = ElectricCar('Tesla', 'Model S', '85kWh');
print(myElectricCar.displayName())
myElectricCar.set_power(100);
print(myElectricCar.get_power())

print(ElectricCar.sampleStaticMethod())

print(myElectricCar.batterySize)

print(isinstance(myElectricCar, Car))
print(isinstance(myElectricCar, ElectricCar))