"""
    Reads ast and returns ist

"""

import ast
from ist import ist_types as it


class Reader(ast.NodeVisitor):
    """
        Reads ast and constructs an ist structure (very similar to the ast)
    """
    operator_map = dict(
        #
        Add      = "+",
        Sub      = "-",
        Mult     = "*",
        Div      = "/",
        Mod      = "%",
        Pow      = "**",

        # binary
        LShift   = "<<",
        RShift   = ">>",
        BitOr    = "|",
        BitXor   = "^",
        BitAnd   = "&",
        FloorDiv = "//",

        # unary
        Invert   = "~",
        Not      = "not",
        UAdd     = "+",
        USub     = "-",

        # boolean
        And      = "&&",
        Or       = "||",

        # compare
        Eq       = "==",
        NotEq    = "!=",
        Lt       = "<",
        LtE      = "<=",
        Gt       = ">",
        GtE      = ">=",
        Is       = "is",
        IsNot    = "is not",
        In       = "in",
        NotIn    = "not in"
    )
    get_operator = lambda self, op: self.operator_map[self.get_name(op)]

    def __init__(self):
        self.collection = {}

    def read(self, name, source):
        """Read the sourcecode and store that as ist."""
        source_ast = ast.parse(source)
        self.collection[name] = self.visit(source_ast)

    def get_name(self, node):
        return node.__class__.__name__

    def visit(self, node):
        name = self.get_name(node)
        
        if isinstance(node, ast.AST) and hasattr(it, name):
            node_type  = getattr(it, name)
            node_attrs = {}

            for fieldname in node._fields:
                field = getattr(node, fieldname)
                if isinstance(field, list):
                    node_attrs[fieldname] = map(self.visit, field)
                else:
                    node_attrs[fieldname] = self.visit(field)

            # create the new node using the attrs.
            node = node_type(**node_attrs)
            visitor = getattr(self, 'visit_{}'.format(name), None)
            if visitor:
                #changing the node
                node = visitor(node)
        # elif not hasattr(it, name):
            # print "not tranforming name", name

        return node

    def visit_AugAssign(self, node):
        """Fixing the operators"""
        return it.AugAssign(
            target = node.target,
            op     = it.operator(type = self.get_operator(node.op)),
            value  = node.value
        )

    def visit_BinOp(self, node):
        """Fixing the operators"""
        return it.BinOp(
            left = node.left,
            op     = it.operator(type = self.get_operator(node.op)),
            right  = node.right
        )

    def visit_UnaryOp(self, node):
        """Fixing the operators"""
        return it.UnaryOp(
            op     = it.operator(type = self.get_operator(node.op)),
            operand  = node.operand
        )

    def visit_BoolOp(self, node):
        """Fixing the operators"""
        return it.BoolOp(
            op     = it.operator(type = self.get_operator(node.op)),
            values  = node.values
        )

    def visit_Compare(self, node):
        """Fixing the operators"""
        return it.Compare(
            left        = node.left,
            ops         = map(lambda op: it.operator(type = self.get_operator(op)), node.ops),
            comparators = node.comparators
        )
