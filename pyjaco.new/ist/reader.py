"""
    Reads ast and returns ist

"""

import ast
from ist import node_types as nt
from ist.util import get_name

class Reader(ast.NodeVisitor):
    def visit(self, node):
        
        name = get_name(node)
        fields = {}

        for field in node._fields:
            value = getattr(node, field)
            if isinstance(value, list):
                fields[field] = self.visit_list(value)

            elif isinstance(value, ast.AST):
                fields[field] = self.visit(value)
            else:
                fields[field] = value

        return getattr(nt, name)(**fields)

    def visit_list(self, list):
        return [self.visit(node) for node in list]
