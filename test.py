a = 100
b = 1000

frac = a/b
print(frac)
percentage = "{:.0%}".format(frac)
percentage = int(percentage[:-1])
percentage += 1
print(percentage)