
from ist.transform import BaseTransformer
import ist.ist_types as it

name = lambda s, ctx=it.Load(): it.Name(s, ctx)


class SemantifyTransformer(BaseTransformer):
    """sematification (SemantifyTransformer) > making sure python's semantics (functions, classes, errorhandling)"""
    
    def trans_Module(self, node):
        return it.Module('test', [it.Call(
            func  = name('PY$Module', it.Load()),
            args = [
                it.FunctionDef(
                    args = name('mod', it.Param()),
                    body = node.body + [
                        it.Return(it.Name("mod"))
                    ]
                )
            ]
        )])

    def trans_Print(self, node):
        assert node.dest == None
        
        return it.Call(
            func  = name('print'),
            args = node.values
        )

    def trans_Name(self, node):
        print "name: {:7}, {}".format(node.id, node.ctx)
        return node

    def trans_FunctionDef(self, node):
        print "Func {}".format(node.name)
        return it.FunctionDef(
            name = node.name,
            decorator_list = node.decorator_list,
            body = [
                it.Assign(
                    targets = [name('params', it.Store())], 
                    value = it.Call(
                        func = name("Arguments"),
                        args = [name("arguments")] + node.args.args
                    )
                )
            ] + node.body
        )

        return node