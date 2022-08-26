def average(*args):
    sum = 0
    for i in args:
        sum += i
    return sum/len(args)

print(average(1, 5, 6, 8, 9, 10))