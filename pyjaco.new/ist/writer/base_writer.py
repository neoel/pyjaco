
class BaseWriter(object):
    indentation = "    "

    def __repr__(self):
        return '\n'.join(self.lines)

    def __init__(self, node):
        self.lines = self.flatten(self.write(node))
    
    def write(self, node):
        name = self.get_name(node) 
        
        writer = getattr(self, "write_{}".format(name), None)
        if writer:
            return writer(node)
            
        print "Could not find writer for:", name
        return ""

    def indent(self, lines):
        return [self.indentation + str(line) for line in self.flatten(lines)]

    def write_lines(self, lines):
        return self.flatten([self.write(line) for line in lines])

    @staticmethod
    def flatten(l):
        r = []  
        for i in l:
            if isinstance(i, list):
                r.extend(BaseWriter.flatten(i))
            else:
                r.append(i)
        return r

    @staticmethod
    def get_name(node):
        return node.__class__.__name__

    def write_str(self, node):
        return node
    def write_NoneType(self, node):
        return node

class NodeWriter(BaseWriter):
    def __getattr__(self, name):
        def write_node(node):
            if hasattr(node, '_fields'):
                name = self.get_name(node)
                fields = []
                for fieldname in node._fields:
                    field = getattr(node, fieldname)

                    if isinstance(field, list):
                        l = self.flatten(['[',self.indent(self.write_lines(field)), ']'])
                    else:
                        l = self.write(field)
                        if not isinstance(l, list):
                            l = [l] 

                    if len(l) == 2:
                        fields.append("{}={}".format(fieldname, ''.join(l)))
                    elif l:
                        fields.append(["{}={}".format(fieldname, l[0]), l[1:]])
                    else:
                        fields.append("{}={}".format(fieldname, repr(l)))

                return self.flatten([
                    name + "(",
                    self.indent(fields),
                    ")"
                ])
            return [repr(node)]
        return write_node


