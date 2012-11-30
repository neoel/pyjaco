
from ist.writer.base_writer import BaseWriter


class JavascriptWriter(BaseWriter):
    
    def write_Module(self, node):
        return map(self.write, node.body)

    def write_Print(self, node):
        return "mod.PY$__builtins__.print({});".format(
            ', '.join(map(self.write, node.values))
        )

    def write_Call(self, node):
        assert node.keywords == []
        assert node.starargs == None
        assert node.kwargs == None
        return "{}({})".format(self.write(node.func), ', '.join(map(self.write, node.args)))

    write_Str  = lambda self, node: repr(node.s)
    write_Name = lambda self, node: node.id
