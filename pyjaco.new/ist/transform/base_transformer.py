
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
    def simple_transformer(self, node):
        """Copy the node, and transform its fields"""

        node_type  = getattr(it, self.get_name(node))

        node_attrs = {}

        for fieldname in node._fields:
            field = getattr(node, fieldname)
            if isinstance(field, list):
                node_attrs[fieldname] = map(self.trans, field)
            else:
                node_attrs[fieldname] = self.trans(field)


        node = node_type(**node_attrs)
        return node


    def trans(self, node):
        """
            It will transform depth first the node, 
            transformer functions should take care of transforming 
        """
        name = self.get_name(node)

        if hasattr(node, '_fields'):

            stats = node.stats

            transformer = getattr(self, 'trans_{}'.format(name), self.simple_transformer)
            
            node = transformer(node)
            if not isinstance(node, (str, list, int)):
                node.stats = stats

        return node
