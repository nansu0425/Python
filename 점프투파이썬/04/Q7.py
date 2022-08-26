data = ""
with open("test.txt", 'r') as f1:
    data = f1.read()
    data = data.replace("java", "python")

with open("test.txt", 'w') as f2:
    f2.write(data)

