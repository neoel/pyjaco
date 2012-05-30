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

var module = __inherit(object, "module");

module.PY$__init__ = function(modname, filename, objects) {
    this.PY$__name__ = modname;
    this.modname = modname;
    this.filename = filename;
    if (objects !== undefined) {
        for (var o in objects) {
            if (o.charAt(2) === "$") {
                this[o] = objects[o];
            }
        }
    }
};

module.__import = function (name, asname) {
    
    // load the object
    var mod = this.__load(name);
    
    // insert the imported module in the current module.
    this["PY$"+(asname||name)] = mod;
    
};
module.__import_from = function (from, name, asname) {
    var modname, loaded_module;
    // the import statement first check's the current module. after that, it checks the global space
//     console.log("from", from, 'import', name);
    
    modname = from + '.' + name;
    
    // import from first
    from = this.__load(from)
    
    loaded_module = __builtins__.PY$getattr(from, name, false);
        
    if (!loaded_module) {
        loaded_module = this.__load(modname);
    }
    if (!loaded_module) {
        throw __builtins__.PY$ImportError("ImportError: Cannot import name "+name);
    }
    
    this["PY$"+(asname||name)] = loaded_module;
};
module.__load = function(name) {
    /**
     * This function loads module name and loads each parentmodule first in order.
     */
    
    var i, mod,nextmod, splitted;
    
    splitted = name.split('.');
    
    for (i=1; i<=splitted.length; i++) {
        if (!mod) {
            mod = this.__load_module(splitted.slice(0, i).join('.'));
        } else {
            nextmod = mod.__load_module(splitted.slice(0, i).join('.'));
            if (!__builtins__.PY$getattr(mod, splitted[i-1], false)) { 
                mod["PY$"+splitted[i-1]] = nextmod;
            }
            mod = nextmod;  
        }
    }
    return mod;
    
};
module.__load_module = function(modname) {
    
    /**
     * Tries to load modname, first from loaded_modules
     */
    var mod, loaded_module;
    /*
    # for each name
    #   = it inside the current module? ( a preloaded variable)
    #   = it part of the current relative path?
    #   = it loaded in loaded_modules
    #   = it available in available_modules
    #   -> Try to call lazy_import
    #   -> Raise error 
    */
    
    if ($PY.loaded_modules.hasOwnProperty(modname)) {
        // search the loaded_modules for the modname
        return $PY.loaded_modules[modname];
    } else if ($PY.available_modules.hasOwnProperty(modname)) {
        // search the available modules for the modname
        mod = $PY.available_modules[modname];
    } else {
        if ($PY.load_lazy) {
            // call the lazy loader
            $PY.load_lazy(modname); // loads the module from the internet, it must be available after it's been called
            
            if ($PY.available_modules.hasOwnProperty(modname)) {
                mod = $PY.available_modules[modname];
            }
        }
    }
    
    // raise error
    if (!mod) {
        return false;
        throw __builtins__.PY$ImportError("ImportError: No module named "+modname);
    }

    if (!!mod) {
        // create the module
        loaded_module = module(mod.name, mod.filename);
        loaded_module.modname = modname;
        
        // insert the module object into loaded_modules.
        $PY.loaded_modules[modname] = loaded_module;
        
        // call the module's body
        mod.body(loaded_module);
    }
    // insert the module in the current.
//     this["PY$"+name] = loaded_module;
    
    return loaded_module;
    
};

module.PY$__getattr__ = function(k) {
    var q = this["PY$" + k];
    if (q === undefined) {
        throw __builtins__.PY$AttributeError(js(this.PY$__repr__()) + " does not have attribute '" + js(k) + "'");
    } else {
        return q;
    }
};

module.PY$__repr__ = function() {
    return str("<module '" + this.modname + "' " + this.filename + ">");
};

module.PY$__str__ = module.PY$__repr__;
