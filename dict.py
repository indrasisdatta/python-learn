employees = {'emp001': 'EmpA', 'emp002': 'EmpB', 'emp003': 'EmpC'}
for emp in employees:
    print(emp, employees[emp])

print('____________')

# Add
employees["emp004"] = 'EmpD'
employees["emp005"] = 'EmpE'
employees["emp006"] = 'EmpF'

# Delete emp004 
employees.pop('emp004')
# Delete last item
employees.popitem()
for empId, empName in employees.items():
    print(empId, empName)