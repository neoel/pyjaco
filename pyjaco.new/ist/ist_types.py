"""Defines all ist nodetypes available"""

from collections import namedtuple

# Add           = namedtuple('Add',           ())
# And           = namedtuple('And',           ())
Assert        = namedtuple('Assert',        ('test', 'msg'))
Assign        = namedtuple('Assign',        ('targets', 'value'))
Attribute     = namedtuple('Attribute',     ('value', 'attr', 'ctx'))
AugAssign     = namedtuple('AugAssign',     ('target', 'op', 'value'))
AugLoad       = namedtuple('AugLoad',       ())
AugStore      = namedtuple('AugStore',      ())
BinOp         = namedtuple('BinOp',         ('left', 'op', 'right'))
# BitAnd        = namedtuple('BitAnd',        ())
# BitOr         = namedtuple('BitOr',         ())
# BitXor        = namedtuple('BitXor',        ())
BoolOp        = namedtuple('BoolOp',        ('op', 'values'))
Break         = namedtuple('Break',         ())
Call          = namedtuple('Call',          ('func', 'args', 'keywords', 'starargs', 'kwargs'))
ClassDef      = namedtuple('ClassDef',      ('name', 'bases', 'body', 'decorator_list'))
Compare       = namedtuple('Compare',       ('left', 'ops', 'comparators'))
Continue      = namedtuple('Continue',      ())
Del           = namedtuple('Del',           ())
Delete        = namedtuple('Delete',        ('targets',))
Dict          = namedtuple('Dict',          ('keys', 'values'))
DictComp      = namedtuple('DictComp',      ('key', 'value', 'generators'))
# Div           = namedtuple('Div',           ())
Ellipsis      = namedtuple('Ellipsis',      ())
# Eq            = namedtuple('Eq',            ())
ExceptHandler = namedtuple('ExceptHandler', ('type', 'name', 'body'))
Exec          = namedtuple('Exec',          ('body', 'globals', 'locals'))
Expr          = namedtuple('Expr',          ('value',))
# Expression    = namedtuple('Expression',    ('body',))
ExtSlice      = namedtuple('ExtSlice',      ('dims',))
# FloorDiv      = namedtuple('FloorDiv',      ())
For           = namedtuple('For',           ('target', 'iter', 'body', 'orelse'))
FunctionDef   = namedtuple('FunctionDef',   ('name', 'args', 'body', 'decorator_list'))
GeneratorExp  = namedtuple('GeneratorExp',  ('elt', 'generators'))
Global        = namedtuple('Global',        ('names',))
# Gt            = namedtuple('Gt',            ())
# GtE           = namedtuple('GtE',           ())
If            = namedtuple('If',            ('test', 'body', 'orelse'))
IfExp         = namedtuple('IfExp',         ('test', 'body', 'orelse'))
Import        = namedtuple('Import',        ('names',))
ImportFrom    = namedtuple('ImportFrom',    ('module', 'names', 'level'))
# In            = namedtuple('In',            ())
Index         = namedtuple('Index',         ('value',))
# Interactive   = namedtuple('Interactive',   ('body',))
# Invert        = namedtuple('Invert',        ())
# Is            = namedtuple('Is',            ())
# IsNot         = namedtuple('IsNot',         ())
# LShift        = namedtuple('LShift',        ())
Lambda        = namedtuple('Lambda',        ('args', 'body'))
List          = namedtuple('List',          ('elts', 'ctx'))
ListComp      = namedtuple('ListComp',      ('elt', 'generators'))
Load          = namedtuple('Load',          ())
# Lt            = namedtuple('Lt',            ())
# LtE           = namedtuple('LtE',           ())
# Mod           = namedtuple('Mod',           ())
Module        = namedtuple('Module',        ('body',))
# Mult          = namedtuple('Mult',          ())
Name          = namedtuple('Name',          ('id', 'ctx'))
# Not           = namedtuple('Not',           ())
# NotEq         = namedtuple('NotEq',         ())
# NotIn         = namedtuple('NotIn',         ())
Num           = namedtuple('Num',           ('n',))
Or            = namedtuple('Or',            ())
Param         = namedtuple('Param',         ())
Pass          = namedtuple('Pass',          ())
# Pow           = namedtuple('Pow',           ())
Print         = namedtuple('Print',         ('dest', 'values', 'nl'))
RShift        = namedtuple('RShift',        ())
Raise         = namedtuple('Raise',         ('type', 'inst', 'tback'))
Repr          = namedtuple('Repr',          ('value',))
Return        = namedtuple('Return',        ('value',))
Set           = namedtuple('Set',           ('elts',))
SetComp       = namedtuple('SetComp',       ('elt', 'generators'))
Slice         = namedtuple('Slice',         ('lower', 'upper', 'step'))
Store         = namedtuple('Store',         ())
Str           = namedtuple('Str',           ('s',))
# Sub           = namedtuple('Sub',           ())
Subscript     = namedtuple('Subscript',     ('value', 'slice', 'ctx'))
# Suite         = namedtuple('Suite',         ('body',))
TryExcept     = namedtuple('TryExcept',     ('body', 'handlers', 'orelse'))
TryFinally    = namedtuple('TryFinally',    ('body', 'finalbody'))
Tuple         = namedtuple('Tuple',         ('elts', 'ctx'))
# UAdd          = namedtuple('UAdd',          ())
# USub          = namedtuple('USub',          ())
UnaryOp       = namedtuple('UnaryOp',       ('op', 'operand'))
While         = namedtuple('While',         ('test', 'body', 'orelse'))
With          = namedtuple('With',          ('context_expr', 'optional_vars', 'body'))
Yield         = namedtuple('Yield',         ('value',))
alias         = namedtuple('alias',         ('name', 'asname'))
arguments     = namedtuple('arguments',     ('args', 'vararg', 'kwarg', 'defaults'))
# boolop        = namedtuple('boolop',        ())
# cmpop         = namedtuple('cmpop',         ())
comprehension = namedtuple('comprehension', ('target', 'iter', 'ifs'))
# excepthandler = namedtuple('excepthandler', ())
# expr          = namedtuple('expr',          ())
# expr_context  = namedtuple('expr_context',  ())
keyword       = namedtuple('keyword',       ('arg', 'value'))
# mod           = namedtuple('mod',           ())
operator      = namedtuple('operator',      ('type'))
# slice         = namedtuple('slice',         ())
# stmt          = namedtuple('stmt',          ())
# unaryop       = namedtuple('unaryop',       ())