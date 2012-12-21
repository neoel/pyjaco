
from tornado import ioloop, web
import os

from start import test

html = """
<!doctype html>
<meta charset='utf-8'/>

<!-- Library -->
{library}

<!-- Python code
{python}
-->

<script>
{javascript}
</script>

"""


class MainHandler(web.RequestHandler):
    library = (
        '05-init',
        '06-pyjaco',
        '10-builtin',
        '11-classes',
        '14-module',
        '22-type-tuple',
        '23-type-list',
        '25-type-str',
        '26-type-number',
        '30-type-int',
    )

    def get(self):
    	python, javascript = test('functions')

        self.write(html.format(
        	javascript = javascript.get('__main__'),
        	python     = python.get('__main__'),
            library    = '\n'.join(map(
                lambda lib: "<script src='/stdlib/{}.js'></script>".format(lib),
                self.library
            ))
        ))


if __name__ == "__main__":
    settings = {
        "debug"         : True
    }

    application = web.Application([
        (r"/", MainHandler),
        (r"/stdlib/(.*)", web.StaticFileHandler, {"path": os.path.abspath("stdlib")}),
    ], **settings)

    application.listen(8002, 'localhost')
    print "Starting server"
    ioloop.IOLoop.instance().start()
