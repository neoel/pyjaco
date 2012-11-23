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
    return False | True


import ast, inspect
from ist.reader import Reader
from ist.writer import Python

#source = inspect.getsource(test)
source = open(__file__).read()
source_ast = ast.parse(source)

reader = Reader()

ist = reader.visit(source_ast)

print ist

print "\n#### Original code: ####"
print source
print "\n#### Transformed code: ####"

print Python(ist)



