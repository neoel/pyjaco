import os
os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

from ist.reader import Reader
from ist.writer import PythonWriter, JavascriptWriter
from ist.transform import __ifyTransformer, TypifyTransformer, SemantifyTransformer

import tornado.autoreload

test = "functions"

print "\n\n########## Translating tests/{}.py:".format(test)

with open("output.js", "w") as output:
    # source = open("base_test.py").read()
    location = "tests/{}.py".format(test)
    source = open(location).read()

    tornado.autoreload.watch(location)

    reader = Reader()
    reader.read('__main__', source)

    transformed = __ifyTransformer(reader.collection).transform()
    transformed = TypifyTransformer(transformed).transform()
    transformed = SemantifyTransformer(transformed).transform()

    python = PythonWriter(reader.collection)
    javascript = JavascriptWriter(transformed)
    
    print "\n########## python code:"
    print python.get('__main__')
    print "\n########## transformed javascript code:"
    print javascript.get('__main__')

    output.write(javascript.get('__main__'))


# import tornado.ioloop
# import tornado.web


# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write(javascript.get('__main__'))


# if __name__ == "__main__":
#     settings = {
#         "debug"         : True
#     }

#     application = tornado.web.Application([
#         (r"/", MainHandler),
#     ], **settings)

#     application.listen(8002, 'localhost')
#     print "Starting server"
#     tornado.ioloop.IOLoop.instance().start()



