

from ist.reader import Reader
from ist.writer import PythonWriter, JavascriptWriter
from ist.transform import __ifyTransformer, TypifyTransformer

test = "getattributes"

print "\n\n########## Translating tests/{}.py:".format(test)

with open("output.py", "w") as output:
    # source = open("base_test.py").read()
    source = open("tests/{}.py".format(test)).read()

    reader = Reader()
    reader.read('__main__', source)

    transformed = __ifyTransformer(reader.collection).transform()
    transformed = TypifyTransformer(transformed).transform()
    # transformed = semantificationTransformer(transformed).transform()

    python = PythonWriter(reader.collection)
    # python2 = PythonWriter(transformormed)
    # javascript = JavascriptWriter(transformed)
    
    print "\n########## python code:"
    print python.get('__main__')
    # print "\n########## transformed python code:"
    # print python2.get('__main__')
    # print "\n########## transformed javascript code:"
    # print javascript.get('__main__')
