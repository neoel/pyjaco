/**
  Copyright 2011 Christian Iversen <ci@sikkerhed.org>
  Copyright 2012 Alexander Esselink <a.esselink@gmail.com>

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

var module = __inherit(object, "module");
var PY$Module = function (module_body) {
    module_body(module());
}

function Arguments(arguments, args, defs, vararg, kwarg) {
    console.log("Creating arguments", arguments, args, defs, vararg, kwarg)
    var i, params;
    params = {}
    for (i=0; i<args.length; i++) {
        if (i in arguments) {
            params["PY$" + args[i]] = arguments[i];
        }
    }
    return params;
}

// module.PY$__init__ = function(modname, filename, objects) {
//     this.modname = modname;
//     this.filename = filename;
//     if (objects !== undefined) {
//         for (var o in objects) {
//             if (o.charAt(2) === "$")
//                 this[o] = objects[o];
//         };
//     }
// };

// module.PY$__getattr__ = function(k) {
//     var q = this["PY$" + k];
//     if (q === undefined) {
//         throw __builtins__.PY$AttributeError(js(this.PY$__repr__()) + " does not have attribute '" + js(k) + "'");
//     } else {
//         return q;
//     }
// };

// module.PY$__repr__ = function() {
//     return str("<module '" + this.modname + "' " + this.filename + ">");
// };

// module.PY$__str__ = module.PY$__repr__;
