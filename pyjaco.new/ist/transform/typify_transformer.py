
from ist.transform import BaseTransformer
import ist.ist_types as it


class TypifyTransformer(BaseTransformer):
    """typeifycation (TypifyTransformer) > explicitly make every literal a python literal. """


    def trans_Str(self, node):
        return it.Call(
            func = it.Name(
                id = "str",
                ctx = it.Load()
            ),
            args = [node],
            keywords = [],
            starargs = None,
            kwargs   = None
        )

    def trans_Num(self, node):
        return it.Call(
            func = it.Name(
                id = "int",
                ctx = it.Load()
            ),
            args = [node],
            keywords = [],
            starargs = None,
            kwargs   = None
        )

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

    # def trans_Call(self, node):
    #     self.print_node(node)
    #     return node
# Call(
#     func=Call(
#         func=Attribute(
#             value=Name(
#                 id=b
#                 ctx=Load()
#             )
#             attr=Call(
#                 func=Name(
#                     id=__getattribute__
#                     ctx=Load()
#                 )
#                 args=[
#                     Str(
#                         s=a
#                     )
#                 ]
#                 keywords=[]
#                 starargs=None
#                 kwargs=None
#             )
#             ctx=Load()
#         )
#         args=[]
#         keywords=[]
#         starargs=None
#         kwargs=None
#     )
#     args=[]
#     keywords=[]
#     starargs=None
#     kwargs=None

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
