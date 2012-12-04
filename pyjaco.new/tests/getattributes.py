

class Test(object):
    def __add__(self, b):
        print "__add__"
        return 2

    def __getattribute__(self, name):
        print name
        return 1

a = 123
b = 54

print "{} + {} = {}".format(a, b,  a + b)
print "{} - {} = {}".format(a, b,  a - b)
print "{} * {} = {}".format(a, b,  a * b)
print "{} / {} = {}".format(a, b,  a / b)
print "{} % {} = {}".format(a, b,  a % b)
print "{} ** {} = {}".format(a, b, a ** b)
print "{} << {} = {}".format(a, b, a << b)
print "{} >> {} = {}".format(a, b, a >> b)
print "{} | {} = {}".format(a, b,  a | b)
print "{} ^ {} = {}".format(a, b,  a ^ b)
print "{} & {} = {}".format(a, b,  a & b)
print "{} // {} = {}".format(a, b, a // b)

c = b.a()()
