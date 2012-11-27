"""
    This is a test file in order to test the new pyjaco ist.

    It will get the source of this file and create an ast.
    That ast will be translated to ist using the Reader class.
    That ist will be written out as python using the writer.Python class.
"""

class FooBar(object):
    def __init__(self):
        pass


def foo(a, *foos, **bars):
    return a

@foo
def test(a, b, bla=3, **foobars):
    """
        Dit is een docstring
    """
    foo(a,
        b, 
        test=bla, 
        *[1, 2, 3], 
        **foobars
    )
    for foobars in foobars[1:   ]:
        if foobar:
            continue
        else:
            if not foobar:
                pass
            elif foobar:    
                print "Bbla"
                break
            print "yeah"
    else:
        if a:
            print "bla"
        else:
            print "Here"

    return False | True
print True or False or False

bla = "1"
bla += "True" if 2 == 4%2 else ""

print set(b for a in range(1, 10) if a % 3 if not a != 2 for b in range(1, 10) if not a % b)

if not bla:
    raise set(False)

print (`bla`,         
        {1, 2, 1, 1, 3, 2, 1}, 
        {i / 2 for i in range(10)},
        +2 - 5
) 
del bla

with open('test.py') as f:
    print "foobar"

while False:
    pass
else:
    print "YEAH"
    print "YEAH"