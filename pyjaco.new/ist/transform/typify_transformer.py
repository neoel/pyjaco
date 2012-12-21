
from ist.transform import BaseTransformer
import ist.ist_types as it


class TypifyTransformer(BaseTransformer):
    """typeifycation (TypifyTransformer) > explicitly make every literal a python literal. """


    def trans_Str(self, node):
        return it.Call(
            func = it.Name("str"),
            args = [node.s]
        )

    def trans_Num(self, node):
        return it.Call(
            func = it.Name("int"),
            args = [node.n]
        )

    def trans_List(self, node):
        return it.Call(
            func = it.Name('list'),
            args = [node.elts]
        )

