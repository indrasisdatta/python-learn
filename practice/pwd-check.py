pwd = input('Enter password:')
if len(pwd) < 6:
    print("Weak")
elif len(pwd) <= 10:
    print("Medium")
else:
    print("Strong")

