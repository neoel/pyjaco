
import tornado.ioloop
import tornado.web

from start import test

html = """
<!doctype html>
<meta charset='utf-8'/>

<!-- Python code
{python}
-->

<script>
{javascript}
</script>

"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	python, javascript = test('all_nodes')




        self.write(html.format(
        	javascript = javascript.get('__main__'),
        	python     = python.get('__main__')
        ))


if __name__ == "__main__":
    settings = {
        "debug"         : True
    }

    application = tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)

    application.listen(8002, 'localhost')
    print "Starting server"
    tornado.ioloop.IOLoop.instance().start()
