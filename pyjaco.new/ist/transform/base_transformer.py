

"""
    A transformer traverses the ist, and then modifies the nodes, requiring them to be recreated.
    This means a transformer must define every node encountered.
"""


import ist.python_types as pt

from ist.writer import NodeWriter

class BaseTransformer(object):

    nw = NodeWriter({})
    def print_node(self, node):
        print '\n'.join(self.nw.write(node))

    def __init__(self, collection):
        self.collection = collection

    def get_name(self, node):
        return node.__class__.__name__

    def transform(self):
        return {
            ist : self.trans(self.collection[ist]) 
                for ist in self.collection
        }
        


    def trans(self, node):
        name = self.get_name(node)
        print name

        if hasattr(node, '_fields'):
            node_type  = getattr(pt, name)
            node_attrs = {}

            for fieldname in node._fields:
                field = getattr(node, fieldname)
                if isinstance(field, list):
                    node_attrs[fieldname] = map(self.trans, field)
                else:
                    node_attrs[fieldname] = self.trans(field)

            # create the new node using the attrs.
            node = node_type(**node_attrs) 
            transformer = getattr(self, 'trans_{}'.format(name), None)
            if transformer:
                #changing the node
                node = transformer(node)
        return node


    def trans_Print(self, node):
        """Print becomes a functioncall to __builtins__.PY$print"""
        return pt.Call(
            func = pt.Name(
                id  = "print",
                ctx = pt.Load()
            ),
            args = node.values,
            keywords = [],
            starargs = None,
            kwargs = None
        )

    # def trans_Call(self, node):
    #     self.print_node(node)
    #     return node

    # def trans_Name(self, node):
    #     self.print_node(node)

    #     return pt.Attribute(
    #         value = pt.Name(
    #             id = 'mod',
    #             ctx = pt.Load()
    #         ),
    #         ctx = node.ctx,
    #         attr = node.id
    #     )

    # def trans_Assign(self, node):
    #     target = node.targets[0]

    #     if isinstance(target, pt.Attribute) and isinstance(target.ctx, pt.Store):
    #         return pt.Attribute(
    #             value = target.value,
    #             ctx   = pt.Load(),
    #             attr  = pt.Call(
    #                 func = pt.Name(
    #                     id = "__setattr__",
    #                     ctx = pt.Load()
    #                 ),
    #                 args = [
    #                     pt.Str(s=target.attr),
    #                     node.value
    #                 ],
    #                 keywords = [],
    #                 starargs = None,
    #                 kwargs   = None
    #             )
    #         )
    #     return node

    # def trans_Attribute(self, node):
    #     if isinstance(node.ctx, pt.Load):
    #         return pt.Attribute(
    #             value = node.value,
    #             ctx   = pt.Load(),
    #             attr  = pt.Call(
    #                 func = pt.Name(
    #                     id = "__getattribute__",
    #                     ctx = pt.Load()
    #                 ),
    #                 args = [pt.Str(s=node.attr)],
    #                 keywords = [],
    #                 starargs = None,
    #                 kwargs   = None
    #             )
    #         )
    #     return node