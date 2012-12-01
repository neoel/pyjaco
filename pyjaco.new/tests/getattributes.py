

class Test(object):
	def __add__(self, b):
		print "__add__"
		return 2

	def __getattribute__(self, name):
		print name
		return 1

a = Test()
b = Test()

print '\n'.join(["'{k}' = {v}" for k, v in {
	"a + b"  : a + b,
	"a - b"  : a - b,
	"a * b"  : a * b,
	"a / b"  : a / b,
	"a % b"  : a % b,
	"a ** b" : a ** b,
	"a << b" : a << b,
	"a >> b" : a >> b,
	"a | b"  : a | b,
	"a ^ b"  : a ^ b,
	"a & b"  : a & b,
	"a // b" : a // b,
}])
