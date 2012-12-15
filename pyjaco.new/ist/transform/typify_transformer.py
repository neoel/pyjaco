
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
