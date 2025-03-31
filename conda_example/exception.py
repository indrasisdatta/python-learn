try:
    file = open('nonexistent-file.txt', 'r')
    # file = open('requirements.txt', 'r')
    content = file.read()
    print(content)
    file.close()
except FileNotFoundError as ex:
    print('File not found')
else:
    print('Else block')
finally:
    print('Finally block')