def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

for x in range(10):
    print 'fib(%d) = %d' % (x, fib(x))