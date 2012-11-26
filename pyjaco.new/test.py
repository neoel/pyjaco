
def foo(a, *foos, **bars):
    return a not in foos

@foo
def test(a, b, bla=3, **foobars):
    foo(a, b, test=bla, *[1, 2, 3], **foobars)
    a + b - bla / a
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



