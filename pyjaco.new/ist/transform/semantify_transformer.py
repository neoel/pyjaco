
from ist.transform import BaseTransformer
import ist.ist_types as it

name = lambda s, ctx=it.Load(): it.Name(s, ctx)


class SemantifyTransformer(BaseTransformer):
    """sematification (SemantifyTransformer) > making sure python's semantics (functions, classes, errorhandling)"""

    space = dict(
        name='__builtins__',
        parent = None,
        vars = {
            'str', 
            'int',
            'list',
            'print'
        }
    )

    def enter_space(self, name):
        # print "Entering namespace", name
        self.space = dict(
            vars = set(),
            name = name,
            parent = self.space
        )

    def leave_space(self, name):
        # print "Leaving space", name, self.space
        self.space = self.space['parent']

    def namespace(name=None):
        """Adds a namespace to the noed, so it can place variables in an object"""
        def space(transformer):
            def spaced_transformer(self, *args, **kwargs):
                self.enter_space(name)
                res = transformer(self, *args, **kwargs)
                self.leave_space(name)
                return res
            spaced_transformer.__name__ = "spaced_" + transformer.__name__
            return spaced_transformer
        return space
    
    @namespace('mod')
    def trans_Module(self, node):
        return it.Module('test', [it.Call(
            func  = name('PY$Module', it.Load()),
            args = [
                it.FunctionDef(
                    args = name('mod', it.Param()),
                    body = map(self.trans, node.body) + [
                        it.Return(it.Name("mod"))
                    ]
                )
            ]
        )])

    def trans_FunctionDef(self, node):
        """take care of the namespacing """
        name = self.trans(node.name)
        decorator_list = map(self.trans, node.decorator_list)
        
        self.enter_space('params')
        args = self.trans(node.args)
        body = map(self.trans, node.body)
        self.leave_space('params')

        return it.FunctionDef(
            name = name,
            decorator_list = decorator_list,
            body = [
                it.Assign(
                    targets = [it.Name('params', it.Store())], 
                    value = it.Call(
                        func = it.Name("Arguments"),
                        args = [it.Name("arguments")] + 
                               [val if val else 'undefined' for val in node.args._asdict().values()]
                    )
                )
            ] + body

        )

    def trans_Print(self, node):
        assert node.dest == None
        
        return it.Call(
            func  = self.trans(name('print')),
            args = map(self.trans, node.values)
        )

    def trans_Name(self, node):
        if isinstance(node.ctx, (it.Store, it.Param)):
            self.space['vars'].add(node.id)
            space = self.space
        elif isinstance(node.ctx, it.Load):
            space = self.space
            while space and node.id not in space['vars']:
                space = space['parent']
        if space:
            id = "{}.PY${}".format(space['name'], node.id)
        else:
            id = "PY${}".format(node.id)
                

        return it.Name(
            ctx = node.ctx,
            id  = id
        )

    # def trans_FunctionDef(self, node):
    #     print "Func {}".format(node.name)
    #     return it.FunctionDef(
    #         name = node.name,
    #         decorator_list = node.decorator_list,
    #         body = [
    #             it.Assign(
    #                 targets = [name('params', it.Store())], 
    #                 value = it.Call(
    #                     func = name("Arguments"),
    #                     args = [name("arguments")] + node.args.args
    #                 )
    #             )
    #         ] + node.body
    #     )

    #     return node