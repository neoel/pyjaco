import os

from ist.reader import Reader
from ist.writer import PythonWriter, JavascriptWriter
from ist.transform import __ifyTransformer, TypifyTransformer, SemantifyTransformer


def test(test_file):
    print "\n\n########## Translating tests/{}.py:".format(test)
    location = "tests/{}.py".format(test_file)
    source = open(location).read()

    reader = Reader()
    reader.read('__main__', source)

    transformed = __ifyTransformer(reader.collection).transform()
    transformed = TypifyTransformer(transformed).transform()
    transformed = SemantifyTransformer(transformed).transform()

    python = PythonWriter(reader.collection)
    javascript = JavascriptWriter(transformed)

    return python, javascript
    

if __name__ == "__main__":
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

    python, javascript = test('functions')

    print "\n########## python code:"
    print python.get('__main__')
    print "\n########## transformed javascript code:"
    print javascript.get('__main__')

    with open("output.js", "w") as output:
        output.write(javascript.get('__main__'))
