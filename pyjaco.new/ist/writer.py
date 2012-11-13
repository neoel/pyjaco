from ist.util import get_name

def flatten(l):
    r = []
    for i in l:
        if isinstance(i, list):
            r.extend(flatten(i))
        else:
            r.append(i)
    return r


class Python(object):
    ''' each line is kept as a string in a list '''
    indentation = "    "

    def __repr__(self):
        return '\n'.join(self.lines)

    def __init__(self, node):
        self.lines = flatten(self.write(node))
    
    def write(self, node):
        name = get_name(node) 
        
        writer = getattr(self, "write_{}".format(name), None)
        if writer:
            return writer(node)

        print "Could not find writer for:", name
        return ""

    def indent(self, lines):
        return [self.indentation + line for line in flatten(lines)]

    def write_lines(self, lines):
        return [self.write(line) for line in lines]

    def write_Module(self, node):
        return self.write_lines(node.body)

    def write_FunctionDef(self, node):
        
#        'name', 'args', 'body', 'decorator_list' 
        lines  = ["@{}".format(self.write(decorator)) for decorator in node.decorator_list]
        lines += ["def {name}({args}):".format(name=node.name, args=self.write(node.args))]
        lines += self.indent(self.write_lines(node.body))

        return lines

    def write_arguments(self, node):
        args = []
        no_defaults = len(node.args) - len(node.defaults)
        
        for i, arg in enumerate(node.args):
            arg = self.write(arg)
            if i < (no_defaults):
                args.append(self.write(arg))
            else:
                default = self.write(node.defaults[i - no_defaults])
                args.append("{}={}".format(arg, default))
        
        if node.vararg:
            args.append("*"  + self.write(node.vararg))
        if node.kwarg:
            args.append("**" + self.write(node.kwarg))

        return ', '.join(args)

    def write_Return(self, node):
        return "return {}".format(self.write(node.value))

    def write_Name(self, node): return node.id
    def write_str(self, node):  return node
    def write_Str(self, node):  return repr(node.s)
    def write_Num(self, node):  return node.n
    def write_BitOr(self, node):  return "or"
    def write_alias(self, node):
        if node.asname:
            return "{} as {}".format(node.name, node.asname)
        return node.name
        
    def write_BinOp(self, node):
        return "{left} {op} {right}".format(
            left  = self.write(node.left),
            op    = self.write(node.op),
            right = self.write(node.right)
        )
    def write_Import(self, node):
        return "import {}".format(', '.join(self.write_lines(node.names)))
    def write_ImportFrom(self, node):
        assert node.level == 0

        return "from {} import {}".format(node.module, ', '.join(self.write_lines(node.names)))

    def write_Assign(self, node):
        return "{targets} = {value}".format(
            targets = ', '.join(self.write_lines(node.targets)),
            value   = self.write(node.value)
        )
    def write_Call(self, node):
#('func', 'args', 'keywords', 'starargs', 'kwargs')
        args  = self.write_lines(node.args)
        args += ["{} = {}".format(self.write(kw.arg), self.write(kw.value)) for kw in node.keywords]
        if node.starargs:
            args.append("*" + self.write(node.starargs))
        if node.kwargs:
            args.append("**" + self.write(node.kwargs))

        return "{}({})".format(self.write(node.func), ', '.join(args))

    def write_Expr(self, node):
        return '' or self.write(node.value)

    def write_List(self, node):
        print node
        return "[{}]".format(', '.join(map(str, self.write_lines(node.elts))))

    def write_Attribute(self, node):
        return "{}.{}".format(self.write(node.value), self.write(node.attr))

    def write_Print(self, node):
        assert node.dest == None
        assert node.nl

        return "print {}".format(', '.join(self.write_lines(node.values)))
