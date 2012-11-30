

from ist.reader import Reader
from ist.writer import PythonWriter, JavascriptWriter
from ist.transform import __ifyTransformer

test = "all_nodes"

print "\n\n########## Translating tests/{}.py:".format(test)

with open("output.py", "w") as output:
    # source = open("base_test.py").read()
    source = open("tests/{}.py".format(test)).read()

    reader = Reader()
    reader.read('__main__', source)

    transformed = __ifyTransformer(reader.collection).transform()
    # transformed = typifyTransformer(transformed).transform()
    # transformed = semantificationTransformer(transformed).transform()

    python = PythonWriter(reader.collection)
    python2 = PythonWriter(transformed)
    javascript = JavascriptWriter(transformed)
    
    print "\n########## python code:"
    print python.get('__main__')
    print "\n########## __ified python code:"
    print python2.get('__main__')
    print "\n########## transformed javascript code:"
    print javascript.get('__main__')
