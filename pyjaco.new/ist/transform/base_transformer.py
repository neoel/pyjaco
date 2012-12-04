
"""
    A transformer traverses the ist, and then modifies the nodes, requiring them to be recreated.
    This means a transformer must define every node encountered.
"""


import ist.ist_types as it

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
            ist: self.trans(self.collection[ist])
                for ist in self.collection
        }

    def trans(self, node):
        name = self.get_name(node)

        if hasattr(node, '_fields'):
            # print self.print_node(node)
            node_type  = getattr(it, name)
            node_attrs = {}

            stats = node.stats

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

            node.stats = stats
        return node
