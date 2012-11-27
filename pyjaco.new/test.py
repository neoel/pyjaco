"""
    This is a test file in order to test the new pyjaco ist.

    It will get the source of this file and create an ast.
    That ast will be translated to ist using the Reader class.
    That ist will be written out as python using the writer.Python class.
"""


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

bla += True if 2 == 4%2 else ""

print set(b for a in range(1, 10) if a % 3 if not a != 2 for b in range(1, 10) if not a % b)

raise set(False)

del bla