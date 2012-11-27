
import ast, inspect
from ist.reader import Reader
from ist.writer import PythonWriter, NodeWriter

source = open("test.py").read()
source_ast = ast.parse(source)

output = open("output.py", "w")

reader = Reader()

ist = reader.visit(source_ast)

print ist

print "\n#### Original code: ####"
print source
print "\n#### Transformed code: ####"

code = repr(PythonWriter(ist))

output.write(code)
output.close()

print code


