
import ast, inspect
from ist.reader import Reader
from ist.writer import PythonWriter, NodeWriter

source = open("test.py").read()
output = open("output.py", "w")

reader = Reader()
reader.read('__main__', source)

writer = PythonWriter(reader.collection)

output.write(writer.get('__main__'))