"""
This file will enumerate over all the ast nodetypes,
It will create a namedtuple for each ast node, using its fields as fields.
The results will be written in `destination_file`
"""


import ast, inspect
from collections import namedtuple

destination_file = 'node_types.py'

used_node_types = [ 
    'Assert', 'Assign', 'Attribute', 'AugAssign', 'AugLoad', 'AugStore', 
    'BinOp', 'BoolOp', 'Break', 
    'Call', 'ClassDef', 'Compare', 'Continue', 
    'Del', 'Delete', 'Dict', 'DictComp', 
    'Ellipsis', 'ExceptHandler', 'Exec', 'Expr', 'ExtSlice', 
    'For', 'FunctionDef', 'GeneratorExp', 'Global', 
    'If', 'IfExp', 'Import', 'ImportFrom', 'Index', 
    'Lambda', 'List', 'ListComp', 'Load', 
    'Module', 'Name', 'Num', 'Or', 'Param', 'Pass', 'Print', 
    'RShift', 'Raise', 'Repr', 'Return', 'Set', 'SetComp', 'Slice', 'Store', 'Str', 'Subscript', 
    'TryExcept', 'TryFinally', 'Tuple', 'UnaryOp', 'While', 'With', 'Yield', 'alias', 'arguments', 'comprehension', 'keyword', 'operator',
]


def get_asttypes():
    astattrs = dir(ast)
    return [nt for nt in astattrs if issubclass(getattr(ast, nt), ast.AST) and nt in used_node_types]

def issubclass(cls, *clsses):
    if inspect.isclass(cls):
        supers = inspect.getmro(cls)
        for s in supers[1:]: # not take this class
            if s in clsses:
                return True
    return False

if __name__ == "__main__":
    with open(destination_file, 'w') as f:
        lines = [
            "from collections import namedtuple", 
            ''
        ]
        for t in get_asttypes():
            lines.append("{name} = ist_node('{name}', **{fields})".format(
                name = t, 
                fields =  {field:None for field in getattr(ast, t)._fields
                }
            ))

        f.write('\n'.join(lines))


