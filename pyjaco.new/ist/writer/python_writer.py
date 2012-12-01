from ist.writer.base_writer import Code, BaseWriter, NodeWriter

class PythonWriter(BaseWriter):
    '''each line is kept as a string in a list'''

    # def write_Add(self, node):
    #     """namedtuple('Add', ())"""
    #     return "+"

    # def write_And(self, node):
    #     """namedtuple('And', ())"""
    #     return "and"

    def write_Assert(self, node):
        """namedtuple('Assert', ('test', 'msg'))"""
        return Code("assert {}".format(self.write(test)), node.stats)

    def write_Assign(self, node):
        """namedtuple('Assign', ('targets', 'value'))"""
        return Code("{targets} = {value}".format(
            targets = self.join(', ', self.write(node.targets)),
            value   = self.write(node.value)
        ), node.stats)

    def write_Attribute(self, node):
        """namedtuple('Attribute', ('value', 'attr', 'ctx'))"""
        return Code("{}.{}".format(self.write(node.value), self.write(node.attr)), node.stats)

    def write_AugAssign(self, node):
        """namedtuple('AugAssign', ('target', 'op', 'value'))"""
        return Code("{} {}= {}".format(self.write(node.target), self.write(node.op), self.write(node.value)), node.stats)

    def write_AugLoad(self, node):
        """namedtuple('AugLoad', ())"""
        pass # context expression nodes

    def write_AugStore(self, node):
        """namedtuple('AugStore',( ))"""
        pass # context expression nodes

    def write_BinOp(self, node):
        """namedtuple('BinOp', ('left', 'op', 'right'))"""
        return Code("{left} {op} {right}".format(
            left  = self.write(node.left),
            op    = self.write(node.op),
            right = self.write(node.right)
        ), node.stats)

    def write_BoolOp(self, node):
        return Code(" {} " .format(
            "and" if self.write(node.op) == "&&" else "or"
        ).join(self.write(node.values)), node.stats)

    def write_Break(self, node):
        """namedtuple('Break', ())"""
        return Code("break", node.stats)

    def write_Call(self, node):
        """namedtuple('Call', ('func', 'args', 'keywords', 'starargs', 'kwargs'))"""
        args  = self.write(node.args)
        args += ["{} = {}".format(self.write(kw.arg), self.write(kw.value)) for kw in node.keywords]
        if node.starargs:
            args.append("*" + self.write(node.starargs))
        if node.kwargs:
            args.append("**" + self.write(node.kwargs))

        return Code("{}({})".format(self.write(node.func), self.join(', ', args)), node.stats)

    def write_ClassDef(self, node):
        """namedtuple('ClassDef', ('name', 'bases', 'body', 'decorator_list'))"""
        return Code([
            ["@{}".format(self.write(decorator)) for decorator in node.decorator_list],
            "class {name}({bases}):".format(
                name=node.name, 
                bases=self.join(', ', self.flatten(self.write(node.bases)))
            ),
            self.indent(self.write(node.body))
        ], node.stats)

    def write_Compare(self, node):
        """namedtuple('Compare', ('left', 'ops', 'comparators'))"""
        # dont know what to expect here
        assert len(node.ops) == 1
        assert len(node.comparators) == 1
        return Code("{} {} {}".format(
            self.write(node.left),
            self.write(node.ops[0]),
            self.write(node.comparators[0])
        ), node.stats)

    def write_Continue(self, node):
        """namedtuple('Continue', ())"""
        return Code(["continue"], node.stats)

    def write_Del(self, node):
        """namedtuple('Del', ())"""
        pass # context expression nodes

    def write_Delete(self, node):
        """namedtuple('Delete', ('targets',))"""
        return Code("del {}".format(self.join(', ', self.write(node.targets))), node.stats)

    def write_Dict(self, node):
        """namedtuple('Dict', ('keys', 'values'))"""
        assert len(node.keys) == len(node.values)

        return Code("{{{}}}".format(
            self.join(', ', [
                "{}:{}".format(self.write(key), self.write(value))
                        for key, value in zip(node.keys, node.values)
            ])
        ), node.stats)

    def write_DictComp(self, node):
        """namedtuple('DictComp', ('key', 'value', 'generators'))"""
        return Code("{{{}:{} {}}}".format(
            self.write(node.key), 
            self.write(node.value), 
            ' '.join(self.write(node.generators))
        ), node.stats)

    # def write_Div(self, node):
    #     """namedtuple('Div', ())"""
    #     return "/"

    def write_Ellipsis(self, node):
        """namedtuple('Ellipsis', ())"""
        return Code("...", node.stats)

    # def write_Eq(self, node):
    #     """namedtuple('Eq', ())"""
    #     return "=="

    def write_ExceptHandler(self, node):
        """namedtuple('ExceptHandler', ('type', 'name', 'body'))"""
        return Code([
            "except {} as {}:".format(self.write(node.type), self.write(node.name))
                if node.type and node.name else
            "except {}:".format(self.write(node.type))
                if node.type else
            "except:",

            self.indent(self.write(node.body))
        ], node.stats)

    def write_Exec(self, node):
        """namedtuple('Exec', ('body', 'globals', 'locals'))"""
        r = "exec {}".format(self.write(node.body))
        if node.globals:
            r += " in {}".format(self.write(node.globals))
        if node.locals:
            r += " , {}".format(self.write(node.locals))
        return Code(r, node.stats)

    def write_Expr(self, node):
        """namedtuple('Expr', ('value',))"""
        return Code('' or self.write(node.value), node.stats)

    # def write_Expression(self, node):
    #     """namedtuple('Expression', ('body',))"""
    #     pass # dont think this wil ever be called (everthing seems a module)

    def write_ExtSlice(self, node):
        """namedtuple('ExtSlice', ('dims',))"""
        return Code(self.join(', ', map(self.write, node.dims)), node.stats)

    # def write_FloorDiv(self, node):
    #     """namedtuple('FloorDiv', ())"""
    #     return "//"

    def write_For(self, node):
        """namedtuple('For', ('target', 'iter', 'body', 'orelse'))"""
        return Code([
            "for {} in {}:".format(self.write(node.target), self.write(node.iter)),
            self.indent(self.write(node.body)),
            "else:",
            self.indent(self.write(node.orelse))
        ], node.stats)

    def write_FunctionDef(self, node):
        """namedtuple('FunctionDef', ('name', 'args', 'body', 'decorator_list'))"""
        return Code([
            ["@{}".format(self.write(decorator)) for decorator in node.decorator_list],
            "def {name}({args}):".format(name=node.name, args=self.write(node.args)),
            self.indent(self.write(node.body))
        ], node.stats)

    def write_GeneratorExp(self, node):
        """namedtuple('GeneratorExp', ('elt', 'generators'))"""
        return Code("({} {})".format(
            self.write(node.elt), 
            ' '.join(self.write(node.generators))
        ), node.stats)

    def write_Global(self, node):
        """namedtuple('Global', ('names',))"""
        return Code("global {}".format(self.join(', ', self.write(node.names))), node.stats)

    # def write_Gt(self, node):
    #     """namedtuple('Gt', ())"""
    #     return ">"

    # def write_GtE(self, node):
    #     """namedtuple('GtE', ())"""
    #     return ">="

    def write_If(self, node):
        """namedtuple('If', ('test', 'body', 'orelse'))"""
        # the if statement
        lines = self.flatten([
            "if {}:".format(self.write(node.test)),
            self.indent(self.write(node.body)),
        ])

        els = self.write(node.orelse)
        if len(node.orelse) == 1 and self.get_name(node.orelse[0]) == "If":
            els[0] = "el" + els[0]
            lines.extend(els)
        elif node.orelse:
            lines.append("else:")
            lines.extend(self.indent(els))

        # else if elif???
        return Code(lines, node.stats)

    def write_IfExp(self, node):
        """namedtuple('IfExp', ('test', 'body', 'orelse'))"""
        r = "{} if {}".format(self.write(node.body), self.write(node.test))
        if node.orelse:
            r += " else {}".format(self.write(node.orelse))
        return Code(r, node.stats)

    def write_Import(self, node):
        """namedtuple('Import', ('names',))"""
        return Code("import {}".format(self.join(', ', self.write(node.names))), node.stats)

    def write_ImportFrom(self, node):
        """namedtuple('ImportFrom', ('module', 'names', 'level'))"""
        assert node.level == 0
        return Code("from {} import {}".format(node.module, self.join(', ', self.write(node.names))), node.stats)

    # def write_In(self, node):
    #     """namedtuple('In', ())"""
    #     return "in"

    def write_Index(self, node):
        """namedtuple('Index', ('value',))"""
        return Code(self.write(node.value), node.stats)

    # def write_Interactive(self, node):
    #     """namedtuple('Interactive', ('body',))"""
    #     pass # dont think this will ever be called (everything is a module)

    # def write_Invert(self, node):
    #     """namedtuple('Invert', ())"""
    #     return "~"

    # def write_Is(self, node):
    #     """namedtuple('Is', ())"""
    #     return "is"

    # def write_IsNot(self, node):
    #     """namedtuple('IsNot', ())"""
    #     return "is not"

    # def write_LShift(self, node):
    #     """namedtuple('LShift', ())"""
    #     return "<<"

    def write_Lambda(self, node):
        """namedtuple('Lambda', ('args', 'body'))"""
        return Code("lambda {}: {}".format(self.write(node.args), self.write(node.body)), node.stats)

    def write_List(self, node):
        """namedtuple('List', ('elts', 'ctx'))"""
        return Code("[{}]".format(self.join(', ', map(str, self.write(node.elts)))), node.stats)

    def write_ListComp(self, node):
        """namedtuple('ListComp', ('elt', 'generators'))"""
        return Code("[{} {}]".format(
            self.write(node.elt), 
            ' '.join(self.write(node.generators))
        ), node.stats)

    def write_Load(self, node):
        """namedtuple('Load', ())"""
        pass # expression context

    # def write_Lt(self, node):
    #     """namedtuple('Lt', ())"""
    #     return "<"

    # def write_LtE(self, node):
    #     """namedtuple('LtE', ())"""
    #     return "<="

    # def write_Mod(self, node):
    #     """namedtuple('Mod', ())"""
    #     return "%"

    def write_Module(self, node):
        """namedtuple('Module', ('body',))"""
        return Code(self.write(node.body), node.stats)

    # def write_Mult(self, node):
    #     """namedtuple('Mult', ())"""
    #     return "*"

    def write_Name(self, node):
        """namedtuple('Name', ('id', 'ctx'))"""
        return Code(node.id, node.stats)

    # def write_Not(self, node):
    #     """namedtuple('Not', ())"""
    #     return "not"

    # def write_NotEq(self, node):
    #     """namedtuple('NotEq', ())"""
    #     return "!="

    # def write_NotIn(self, node):
    #     """namedtuple('NotIn', ())"""
    #     return "not in"

    def write_Num(self, node):
        """namedtuple('Num', ('n',))"""
        return Code(str(node.n), node.stats)

    def write_Or(self, node):
        """namedtuple('Or', ())"""
        return Code("or", node.stats)

    def write_Param(self, node):
        """namedtuple('Param', ())"""
        pass # expression context node

    def write_Pass(self, node):
        """namedtuple('Pass', ())"""
        return Code("pass", node.stats)

    # def write_Pow(self, node):
    #     """namedtuple('Pow', ())"""
    #     return "**"

    def write_Print(self, node):
        """namedtuple('Print', ('dest', 'values', 'nl'))"""
        assert node.dest == None
        assert node.nl
        return Code("print {}".format(self.join(', ', self.write(node.values))), node.stats)

    def write_RShift(self, node):
        """namedtuple('RShift', ())"""
        return Code(">>", node.stats)

    def write_Raise(self, node):
        """namedtuple('Raise', ('type', 'inst', 'tback'))"""
        assert node.inst is None
        assert node.tback is None

        return Code("raise {}".format(self.write(node.type) if node.type else ""), node.stats)

    def write_Repr(self, node):
        """namedtuple('Repr', ('value',))"""
        return Code("`{}`".format(self.write(node.value)), node.stats)

    def write_Return(self, node):
        """namedtuple('Return', ('value',))"""
        return Code("return {}".format(self.write(node.value)), node.stats)

    def write_Set(self, node):
        """namedtuple('Set', ('elts',))"""
        return Code("{{{}}}".format(self.join(', ', map(self.write, node.elts))), node.stats)

    def write_SetComp(self, node):
        """namedtuple('SetComp', ('elt', 'generators'))"""
        return Code("{{{} {}}}".format(self.write(node.elt), ' '.join(map(self.write, node.generators))), node.stats)

    def write_Slice(self, node):
        """namedtuple('Slice', ('lower', 'upper', 'step'))"""  
        slice_el = lambda n: n if n != "None" and n else ""
        return Code(":".join(
                map(
                    slice_el, 
                    map(
                        self.write, 
                        [node.lower, node.upper, node.step]
                    )
                )
        )   , node.stats)

    def write_Store(self, node):
        """namedtuple('Store', ())"""
        pass # expression context

    def write_Str(self, node):
        """namedtuple('Str', ('s',))"""
        return Code(repr(node.s), node.stats)

    # def write_Sub(self, node):
    #     """namedtuple('Sub', ())"""
    #     return "-"

    def write_Subscript(self, node):
        """namedtuple('Subscript', ('value', 'slice', 'ctx'))"""
        return Code("{}[{}]".format(self.write(node.value), self.write(node.slice)), node.stats)

    # def write_Suite(self, node):
    #     """namedtuple('Suite', ('body',))"""
    #     pass # something to do with jython

    def write_TryExcept(self, node):
        """namedtuple('TryExcept', ('body', 'handlers', 'orelse'))"""
        return Code([
            "try:",
            self.indent(self.write(node.body)),
            map(self.write, node.handlers),

            ["else:", self.indent(self.write(node.orelse))]
                if node.orelse else
            []
        ], node.stats)

    def write_TryFinally(self, node):
        """namedtuple('TryFinally', ('body', 'finalbody'))"""
        return Code([
            self.write(node.body[0]) 
                if len(node.body) == 1 and self.get_name(node.body[0]) == "TryExcept" else
            ["try:", self.indent(self.write(node.body))],
            "finally:",
            self.indent(self.write(node.finalbody))
        ], node.stats)

    def write_Tuple(self, node):
        """namedtuple('Tuple', ('elts', 'ctx'))"""
        return Code("({})".format(self.join(', ', self.write(node.elts))), node.stats)

    # def write_UAdd(self, node):
    #     """namedtuple('UAdd', ())"""
    #     return "+"

    # def write_USub(self, node):
    #     """namedtuple('USub', ())"""
    #     return "-"

    def write_UnaryOp(self, node):
        """namedtuple('UnaryOp', ('op', 'operand'))"""
        return Code("{} {}".format(self.write(node.op), self.write(node.operand)), node.stats)

    def write_While(self, node):
        """namedtuple('While', ('test', 'body', 'orelse'))"""
        r = [
            "while {}:".format(self.write(node.test)),
            self.indent(map(self.write, node.body)),
        ]
        if node.orelse:
            r.extend([
                "else:",
                self.indent(map(self.write, node.orelse))
            ])
        return Code(r, node.stats)

    def write_With(self, node):
        """namedtuple('With', ('context_expr', 'optional_vars', 'body'))"""
        w = "with {}".format(self.write(node.context_expr))

        if node.optional_vars:
            w += " as {}".format(self.write(node.optional_vars))
        return Code([
            "{}:".format(w),
            self.indent(map(self.write, node.body))
        ], node.stats)

    def write_Yield(self, node):
        """namedtuple('Yield', ('value',))"""
        return Code("yield {}".format(self.write(node.value)), node.stats)

    def write_alias(self, node):
        """namedtuple('alias', ('name', 'asname'))"""
        if node.asname:
            return Code("{} as {}".format(node.name, node.asname), node.stats)
        return Code(node.name, node.stats)

    def write_arguments(self, node):
        """namedtuple('arguments', ('args', 'vararg', 'kwarg', 'defaults'))"""
        args = []
        no_defaults = len(node.args) - len(node.defaults)
        
        for i, arg in enumerate(node.args):
            arg = self.write(arg)
            if i < (no_defaults):
                args.append(self.write(arg))
            else:
                default = self.write(node.defaults[i - no_defaults])
                args.append("{}={}".format(arg, default))
        if node.vararg:
            args.append("*"  + self.write(node.vararg))
        if node.kwarg:
            args.append("**" + self.write(node.kwarg))

        return Code(self.join(', ', args), node.stats)

    # def write_boolop(self, node):
    #     """namedtuple('boolop', ())"""
    #     raise NotImplementedError
 
    # def write_cmpop(self, node):
    #     """namedtuple('cmpop', ())"""
    #     raise NotImplementedError

    def write_comprehension(self, node):
        """namedtuple('comprehension', ('target', 'iter', 'ifs'))"""
        r = "for {} in {}".format(self.write(node.target), self.write(node.iter))
        for i in node.ifs:
            r += " if {}".format(self.write(i))
        return Code(r, node.stats)

    # def write_excepthandler(self, node):
    #     """namedtuple('excepthandler', ())"""
    #     raise NotImplementedError

    # def write_expr(self, node):
    #     """namedtuple('expr', ())"""
    #     raise NotImplementedError

    # def write_expr_context(self, node):
    #     """namedtuple('expr_context', ())"""
    #     raise NotImplementedError

    # def write_keyword(self, node):
    #     """namedtuple('keyword', ('arg', 'value'))"""
    #     raise NotImplementedError

    # def write_mod(self, node):
    #     """namedtuple('mod', ())"""
    #     raise NotImplementedError

    def write_operator(self, node):
        """namedtuple('operator', ())"""
        return Code(node.type, node.stats)
 
    # def write_slice(self, node):
    #     """namedtuple('slice', ())"""
    #     raise NotImplementedError

    # def write_stmt(self, node):
    #     """namedtuple('stmt', ())"""
    #     raise NotImplementedError

    # def write_unaryop(self, node):
    #     """namedtuple('unaryop', ())"""
    #     raise NotImplementedError