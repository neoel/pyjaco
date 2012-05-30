######################################################################
##
## Copyright 2010-2011 Ondrej Certik <ondrej@certik.cz>
## Copyright 2010-2011 Mateusz Paprocki <mattpap@gmail.com>
## Copyright 2011 Christian Iversen <ci@sikkerhed.org>
##
## Permission is hereby granted, free of charge, to any person
## obtaining a copy of this software and associated documentation
## files (the "Software"), to deal in the Software without
## restriction, including without limitation the rights to use,
## copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following
## conditions:
##
## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
## OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
## HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
## WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
## OTHER DEALINGS IN THE SOFTWARE.
##
######################################################################

import ast
import inspect

class Scope(object):
    
    def __init__(self, type):
        self.type = type
        
        self.variables = []
        self.classes = {}
        self.exceptions = []
        self.funcs = []
        
        self._scopes = []
        
        self = object()
    
    def enter(self, type):
        
        self._scopes.append({
            'variables'  : self.variables,
            'classes'    : self.classes,
            'exceptions' : self.exceptions,
            'funcs'      : self.funcs,
            'type'       : self.type
        })
        
        self.variables = []
        self.classes = {}
        self.exceptions = []
        self.funcs = []
        self.type = type
        
        return self
        
    def leave(self):
        
        s = self._scopes.pop(-1)
        
        self.variables  = s['variables']
        self.classes    = s['classes']
        self.exceptions = s['exceptions']
        self.funcs      = s['funcs']
        
        self.type       = s['type']
        
        return self
        
    def parent_type(self):
        return self._scopes[-1]['type']
        
    def contains(self, name):
        if (name in self.variables) or (name in self.classes) or (name in self.funcs):
            return True
       
        for scope in self._scopes[::-1]:
            if name in scope['variables']:
                return True
            elif name in scope['classes']:
                return True
            elif name in scope['funcs']:
                return True
    
    def find_scope_for(self, name):
        """Search the scope in which name is first encountered"""
        
        if (name in self.variables) or (name in self.classes) or (name in self.funcs):
            return self.type
       
        for scope in self._scopes[::-1]:
            if (name in scope['variables']) or (name in scope['classes']) or (name in scope['funcs']):
                return scope['type']
    
    def fetch_name(self, name):
        
        scopetype = self.find_scope_for(name)
        
        if scopetype == 'builtin':
            name =  "__builtins__.PY$" + name
        elif scopetype == 'module':
            name = "mod.PY$" + name
            
        return name
         
    def remove(self, name):
        
        if   name in self.variables:
            self.variables.remove(name)
        elif name in self.classes:
            del self.classes[name]
        elif name in self.funcs:
            self.funcs.remove(name)
            
        else:
            for scope in self._scopes[::-1]:
                
                if name in scope['variables']:
                    scope['variables'].remove(name)
                elif name in scope['classes']:
                    del scope['classes'][name]
                elif name in scope['funcs']:
                    scope['funcs'].remove(name)
       
        

class JSError(Exception):
    pass

class BaseCompiler(object):

    name_map = {
        'super' : 'Super',
        'delete': '__delete',
        'default': '__default',
    }

    import __builtin__
    builtin = set([x for x in dir(__builtin__) if not x.startswith("__")])

    def __init__(self, opts, scope=None):
        self.index_var = 0
        # This is the name of the classes that we are currently in:
        self._class_name = []
        
        # Keep track of the different scopes.
        if scope:
            self.scope = scope
        else:
            self.scope = Scope('builtin')
            self.scope.variables.extend(self.builtin)
            # This lists all variables in the local scope:
        
        self.opts = opts
        
    def enter_scope(self, type):
        self.scope = self.scope.enter(type)
    
    def leave_scope(self):
        self.scope = self.scope.leave()

    def alloc_var(self):
        self.index_var += 1
        return "$v%d" % self.index_var

    def visit(self, node):
        try:
            visitor = getattr(self, 'visit_' + self.name(node))
        except AttributeError:
            raise JSError("syntax not supported (%s: %s)" % (node.__class__.__name__, node))

        return visitor(node)

    @staticmethod
    def indent(stmts):
        return [ "    " + stmt for stmt in stmts ]

    ## Shared code

    @staticmethod
    def name(node):
        return node.__class__.__name__

    ## Shared visit functions

    def visit_AssignSimple(self, target, value):
        raise NotImplementedError()

    def visit_Assign(self, node):
        if len(node.targets) > 1:
            tmp = self.alloc_var()
            q = ["var %s = %s" % (tmp, self.visit(node.value))]
            for t in node.targets:
                q.extend(self.visit_AssignSimple(t, tmp))
            return q
        else:
            return self.visit_AssignSimple(node.targets[0], self.visit(node.value))

    def _visit_Exec(self, node):
        pass

    def visit_Print(self, node):
        assert node.dest is None
        assert node.nl
        values = [self.visit(v) for v in node.values]
        values = ", ".join(values)
        return ["__builtins__.PY$print(%s);" % values]

    def visit_Module(self, node, name, filename=None):
        self.enter_scope("module")
        
        module = ["$PY.add_module('{name}', '{filename}', function (mod) {{".format(name=name, filename=filename)]
        
        for stmt in node.body:
            module.extend(self.indent(self.visit(stmt)))

        module.extend(["});"])
        self.leave_scope()
        return module

    def visit_Assert(self, node):
        test = self.visit(node.test)

        if node.msg is not None:
            return ["assert(%s, %s);" % (test, self.visit(node.msg))]
        else:
            return ["assert(%s);" % test]

    def visit_Return(self, node):
        if node.value is not None:
            return ["return %s;" % self.visit(node.value)]
        else:
            return ["return;"]

    def visit_Expr(self, node):
        return [self.visit(node.value) + ";"]

    def visit_Pass(self, node):
        return ["/* pass */"]

    def visit_Break(self, node):
        return ["break;"]

    def visit_Continue(self, node):
        return ["continue;"]

    def visit_arguments(self, node):
        return ", ".join([self.visit(arg) for arg in node.args])
