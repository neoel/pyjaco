
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
        return [self.indentation + line for line in self.flatten(lines)]

    def write_lines(self, lines):
        return [self.write(line) for line in lines]

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