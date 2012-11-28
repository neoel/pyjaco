
import ast, inspect

from ist.reader import Reader
from ist.writer import PythonWriter, NodeWriter
from ist.transform import BaseTransformer

with open("output.py", "w") as output:
	source = open("base_test.py").read()

	reader = Reader()
	reader.read('__main__', source)

	transformer = BaseTransformer(reader.collection)

	writerClass =  PythonWriter

	# writer = PythonWriter(transformer.transform())
	writer1 = writerClass(reader.collection)
	writer2 = writerClass(transformer.transform())


	print writer1.get('__main__')
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print writer2.get('__main__')

	output.write(writer2.get('__main__'))