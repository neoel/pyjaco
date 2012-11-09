/**
  Copyright 2011 Christian Iversen <ci@sikkerhed.org>

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation
  files (the "Software"), to deal in the Software without
  restriction, including without limitation the rights to use,
  copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
  OTHER DEALINGS IN THE SOFTWARE.
**/

var Exception = __inherit(object, "Exception");

Exception.PY$__init__ = function() {
    if (arguments.length > 0) {
        this.PY$message = arguments[0];
    } else {
        this.PY$message = "";
    }
    this.message = "pyjaco: " + js(this.PY$__class__.PY$__name__) + ": " + js(this.PY$message);
};

Exception.PY$__str__ = function() {
    return str(this.PY$message);
};

__builtins__.PY$__exceptions__ = [
    'NotImplementedError',
    'ZeroDivisionError',
    'AssertionError',
    'AttributeError',
    'RuntimeError',
    'ImportError',
    'TypeError',
    'ValueError',
    'NameError',
    'IndexError',
    'KeyError',
    'StopIteration',
    'IOError'
];

for (var i in __builtins__.PY$__exceptions__) {
    __builtins__["PY$" + __builtins__.PY$__exceptions__[i]] = __inherit(Exception, __builtins__.PY$__exceptions__[i]);
}

$PY.c_stopiter = __builtins__.PY$StopIteration("No more items");
