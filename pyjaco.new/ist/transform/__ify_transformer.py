from ist.transform import BaseTransformer
import ist.ist_types as it


class __ifyTransformer(BaseTransformer):
    """__ification (__ifyTransformer) > adding all the magic methods."""

    # def trans_Print(self, node):
    #     """Print becomes a functioncall to __builtins__.PY$print"""
    #     return it.Call(
    #         func = it.Name(
    #             id  = "print",
    #             ctx = it.Load()
    #         ),
    #         args = node.values,
    #         keywords = [],
    #         starargs = None,
    #         kwargs = None
    #     )

    # def trans_Call(self, node):
    #     self.print_node(node)
    #     return node

    # def trans_Name(self, node):
    #     self.print_node(node)

    #     return it.Attribute(
    #         value = it.Name(
    #             id = 'mod',
    #             ctx = it.Load()
    #         ),
    #         ctx = node.ctx,
    #         attr = node.id
    #     )

    # op methods
    bin_op_map = {
        '+': "__add__",
        '-': "__sub__",
        '*': "__mul__",
        '/': "__div__",
        '%': "__mod__",
        '**': "__pow__",
        '<<': "__lshift__",
        '>>': "__rshift__",
        '|': "__or__",
        '^': "__xor__",
        '&': "__and__",
        '//': "__floordiv__"
    }

    def trans_BinOp(self, node):
        return it.Attribute(
            value = node.left,
            ctx   = it.Load(),
            attr  = it.Call(
                func = it.Name(
                    id = self.bin_op_map[node.op.type],
                    ctx = it.Load()
                ),
                args = [node.right],
                keywords = [],
                starargs = None,
                kwargs   = None
            )
        )

    def trans_Attribute(self, node):
        if isinstance(node.ctx, it.Load):
            if isinstance(node.attr, it.Call):
                return it.Attribute(
                    value = node.value,
                    ctx   = it.Load(),
                    attr  = it.Call(
                        func = it.Call(
                            func = it.Name(
                                id = "__getattribute__",
                                ctx = it.Load()
                            ),
                            args = [it.Str(s=node.attr.func.id)],
                            keywords = [],
                            starargs = None,
                            kwargs   = None
                        ),
                        args = node.attr.args,
                        keywords = [],
                        starargs = None,
                        kwargs   = None
                    )
                )
            else:
                return it.Attribute(
                    value = node.value,
                    ctx   = it.Load(),
                    attr  = it.Call(
                        func = it.Name(
                            id = "__getattribute__",
                            ctx = it.Load()
                        ),
                        args = [it.Str(s=node.attr)],
                        keywords = [],
                        starargs = None,
                        kwargs   = None
                    )
                )
        return node


    def trans_Assign(self, node):
        target = node.targets[0]

        if isinstance(target, it.Attribute) and isinstance(target.ctx, it.Store):
            return it.Attribute(
                value = target.value,
                ctx   = it.Load(),
                attr  = it.Call(
                    func = it.Name(
                        id = "__setattr__",
                        ctx = it.Load()
                    ),
                    args = [
                        it.Str(s=target.attr),
                        node.value
                    ],
                    keywords = [],
                    starargs = None,
                    kwargs   = None
                )
            )
        return node
