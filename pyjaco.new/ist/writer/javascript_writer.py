
from ist.writer.base_writer import BaseWriter
import json


class JavascriptWriter(BaseWriter):
    
    write_Num = lambda self, node: str(node.n)
    write_Str  = lambda self, node: repr(node.s)
    write_Name = lambda self, node: node.id
    write_Return = lambda self, node: "return {}".format(self.write(node.value))

    def write_Module(self, node):
        print "Module", node.stats
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

    def write_Assign(self, node):
        assert len(node.targets) == 1

        return "var {} = {}".format(self.write(node.targets[0]), self.write(node.value))

    def write_Attribute(self, node):
        return "{}.{}".format(self.write(node.value), self.write(node.attr))
        self.print_node(node)

    def write_ClassDef(self, node):
        # name, bases, body, decorator_list
        return "{} = ClassDef({}, {}, {})".format(
            node.name, node.name,
            self.write(node.bases),
            json.dumps([
                self.write(attr) 
                    for attr in node.body
            ])
        )

    def write_FunctionDef(self, node):
        # name, args, body, decorator_list
        return ["{} = function ({}) {{".format(
                    node.name,
                    ', '.join(self.write(node.args))
                ),
                self.indent(map(self.write, node.body)),
                "};"
        ]

    def write_arguments(self, node):
        assert node.vararg   == None
        assert node.kwarg    == None
        assert node.defaults == []

        return map(self.write, node.args)



    

