from ist import ist_types as it
from ist.writer.base_writer import BaseWriter
import json


class JavascriptWriter(BaseWriter):
    
    write_Num = lambda self, node: str(node.n)
    write_Str  = lambda self, node: repr(node.s)
    write_Name = lambda self, node: node.id
    write_Return = lambda self, node: "return {}".format(self.write(node.value))

    def write_Module(self, node):
        return map(self.write, node.body)

    def write_Name(self, node):
        return node.id

    def write_Call(self, node):
        assert node.keywords == []
        assert node.starargs == None
        assert node.kwargs == None

        return "{}({})".format(self.write(node.func), ', '.join(map(self.write, node.args)))

    def write_Assign(self, node):
        assert len(node.targets) == 1

        return "var {} = {}".format(self.write(node.targets[0]), self.write(node.value))

    def write_Attribute(self, node):
        print "Attribute: {}, {}".format(self.write(node.attr), node.ctx)
        return "{}.{}".format(self.write(node.value), self.write(node.attr))

    def write_FunctionDef(self, node):
        # name, args, body, decorator_list
        if node.name:
            return self.join([
                        "{} = function ({}) {{".format(
                            self.write(node.name),
                            self.write(node.args)
                        ),
                        self.indent(
                            map(self.write, node.body)
                        ),
                        "}"
            ])
        else:
            return self.join([
                "function ({}) {{".format(self.write(node.args)),
                self.indent(
                    map(self.write, node.body)
                ),
                "}"
            ])


    def write_arguments(self, node):
        assert node.vararg   == None
        assert node.kwarg    == None
        assert node.defaults == []

        return ','.join(map(self.write, node.args))

    def write_Expr(self, node):
        return '' or self.write(node.value)


    

