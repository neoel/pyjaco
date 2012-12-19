

class BaseWriter(object):
    indentation = "    "
    
    def print_node(self, node):
        nw = NodeWriter({})
        print '\n'.join(nw.write(node))

    def __repr__(self):
        return '\n'.join(self.lines)

    def __init__(self, collection):
        self.collection = collection

    def get(self, name):
        """Gets the ist of `name` and returns that as a string"""
        ist = self.collection.get(name)

        if ist:
            return self.join(self.write(ist))
        else:
            raise AttributeError("Could not find {}".format(name))
    
    def write(self, node):
        if node:
            name = self.get_name(node)
            
            writer = getattr(self, "write_{}".format(name), None)
            if writer:
                return self.flatten(writer(node))
            elif isinstance(node, list):
                return map(self.write, node)
            elif not node or isinstance(node, str):
                return node 
            else:
                raise ValueError("{}: write_{} not found".format(self.get_name(self), name))
        else:
            return ''

    def join(self, list):
        return '\n'.join(self.flatten(list))

    def indent(self, lines):
        lns = []
        for line in self.flatten(lines):
            lns += line.split('\n');

        return [self.indentation + str(line) for line in lns]

    def write_lines(self, lines):
        return self.flatten(map(self.write, lines))

    @staticmethod
    def flatten(l):
        r = []
        if isinstance(l, list):
            for i in l:
                if isinstance(i, list):
                    r.extend(BaseWriter.flatten(i))
                else:
                    r.append(i)
            return r
        return l

    @staticmethod
    def get_name(node):
        return node.__class__.__name__



class NodeWriter(BaseWriter):
    def __getattr__(self, name):
        def write_node(node):
            if hasattr(node, '_fields'):
                name = self.get_name(node)
                fields = []
                for fieldname in node._fields:
                    field = getattr(node, fieldname)

                    if isinstance(field, list):
                        l = self.flatten(['[', self.indent(self.write_lines(field)), ']'])
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
