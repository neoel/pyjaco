from ist.writer.base_writer import BaseWriter, NodeWriter


class PythonWriter(BaseWriter):
    ''' each line is kept as a string in a list '''
  

    def write_Add(self, node):
        """namedtuple('Add', ())"""
        return "+"

    def write_And(self, node):
        """namedtuple('And', ())"""
        return "and"

    def write_Assert(self, node):
        """namedtuple('Assert', ('test', 'msg'))"""
        return "assert {}".format(self.write(test))

    def write_Assign(self, node):
        """namedtuple('Assign', ('targets', 'value'))"""
        return "{targets} = {value}".format(
            targets = ', '.join(self.write_lines(node.targets)),
            value   = self.write(node.value)
        )

    def write_Attribute(self, node):
        """namedtuple('Attribute', ('value', 'attr', 'ctx'))"""
        return "{}.{}".format(self.write(node.value), self.write(node.attr))

    def write_AugAssign(self, node):
        """namedtuple('AugAssign', ('target', 'op', 'value'))"""
        return "{} {}= {}".format(self.write(node.target), self.write(node.op), self.write(node.value))

    def write_AugLoad(self, node):
        """namedtuple('AugLoad', ())"""
        raise NotImplementedError

    def write_AugStore(self, node):
        """namedtuple('AugStore', ())"""
        raise NotImplementedError

    def write_BinOp(self, node):
        """namedtuple('BinOp', ('left', 'op', 'right'))"""
        return "{left} {op} {right}".format(
            left  = self.write(node.left),
            op    = self.write(node.op),
            right = self.write(node.right)
        )

    def write_BitAnd(self, node):
        """namedtuple('BitAnd', ())"""
        return "&"

    def write_BitOr(self, node):
        """namedtuple('BitOr', ())"""
        return "|"

    def write_BitXor(self, node):
        """namedtuple('BitXor', ())"""
        return "^"

    def write_BoolOp(self, node):
        """namedtuple('BoolOp', ('op', 'values'))"""
        return " {} " .format(self.write(node.op)).join(map(self.write, node.values))

    def write_Break(self, node):
        """namedtuple('Break', ())"""
        return "break"

    def write_Call(self, node):
        """namedtuple('Call', ('func', 'args', 'keywords', 'starargs', 'kwargs'))"""
        args  = self.write_lines(node.args)
        args += ["{} = {}".format(self.write(kw.arg), self.write(kw.value)) for kw in node.keywords]
        if node.starargs:
            args.append("*" + self.write(node.starargs))
        if node.kwargs:
            args.append("**" + self.write(node.kwargs))

        return "{}({})".format(self.write(node.func), ', '.join(args))

    def write_ClassDef(self, node):
        """namedtuple('ClassDef', ('name', 'bases', 'body', 'decorator_list'))"""
        raise NotImplementedError

    def write_Compare(self, node):
        """namedtuple('Compare', ('left', 'ops', 'comparators'))"""
        # dont know what to expect here
        assert len(node.ops) == 1
        assert len(node.comparators) == 1
        return "{} {} {}".format(
            self.write(node.left),
            self.write(node.ops[0]),
            self.write(node.comparators[0])
        )

    def write_Continue(self, node):
        """namedtuple('Continue', ())"""
        return ["continue"]

    def write_Del(self, node):
        """namedtuple('Del', ())"""
        raise NotImplementedError

    def write_Delete(self, node):
        """namedtuple('Delete', ('targets',))"""
        return "del {}".format(', '.join(map(self.write, node.targets)))

    def write_Dict(self, node):
        """namedtuple('Dict', ('keys', 'values'))"""
        raise NotImplementedError

    def write_DictComp(self, node):
        """namedtuple('DictComp', ('key', 'value', 'generators'))"""
        return "{{{}:{} {}}}".format(
            self.write(node.key), 
            self.write(node.value), 
            ' '.join(map(self.write, node.generators))
        )

    def write_Div(self, node):
        """namedtuple('Div', ())"""
        return "/"

    def write_Ellipsis(self, node):
        """namedtuple('Ellipsis', ())"""
        return "..."

    def write_Eq(self, node):
        """namedtuple('Eq', ())"""
        return "=="

    def write_ExceptHandler(self, node):
        """namedtuple('ExceptHandler', ('type', 'name', 'body'))"""
        raise NotImplementedError

    def write_Exec(self, node):
        """namedtuple('Exec', ('body', 'globals', 'locals'))"""
        raise NotImplementedError

    def write_Expr(self, node):
        """namedtuple('Expr', ('value',))"""
        return '' or self.write(node.value)

    def write_Expression(self, node):
        """namedtuple('Expression', ('body',))"""
        raise NotImplementedError

    def write_ExtSlice(self, node):
        """namedtuple('ExtSlice', ('dims',))"""
        raise NotImplementedError

    def write_FloorDiv(self, node):
        """namedtuple('FloorDiv', ())"""
        raise NotImplementedError

    def write_For(self, node):
        """namedtuple('For', ('target', 'iter', 'body', 'orelse'))"""
        return self.flatten([
            "for {} in {}:".format(self.write(node.target), self.write(node.iter)),
            self.indent(self.write_lines(node.body)),
            "else:",
            self.indent(self.write_lines(node.orelse))
        ])

    def write_FunctionDef(self, node):
        """namedtuple('FunctionDef', ('name', 'args', 'body', 'decorator_list'))"""
        return self.flatten([
            ["@{}".format(self.write(decorator)) for decorator in node.decorator_list],
            ["def {name}({args}):".format(name=node.name, args=self.write(node.args))],
            self.indent(self.write_lines(node.body))
        ])

    def write_GeneratorExp(self, node):
        """namedtuple('GeneratorExp', ('elt', 'generators'))"""
        return "({} {})".format(
            self.write(node.elt), 
            ' '.join(map(self.write, node.generators))
        )

    def write_Global(self, node):
        """namedtuple('Global', ('names',))"""
        return "global {}".format(', '.join(map(self.write, node.names)))

    def write_Gt(self, node):
        """namedtuple('Gt', ())"""
        return ">"

    def write_GtE(self, node):
        """namedtuple('GtE', ())"""
        return ">="

    def write_If(self, node):
        """namedtuple('If', ('test', 'body', 'orelse'))"""
        # the if statement
        lines = self.flatten([
            "if {}:".format(self.write(node.test)),
            self.indent(self.write_lines(node.body)),
        ])

        els = self.write_lines(node.orelse)
        if len(node.orelse) == 1 and self.get_name(node.orelse[0]) == "If":
            els[0] = "el" + els[0]
            lines.extend(els)
        elif node.orelse:
            lines.append("else:")
            lines.extend(self.indent(els))

        # else if elif???
        return lines

    def write_IfExp(self, node):
        """namedtuple('IfExp', ('test', 'body', 'orelse'))"""
        r = "{} if {}".format(self.write(node.body), self.write(node.test))
        if node.orelse:
            r += " else {}".format(self.write(node.orelse))
        return r

    def write_Import(self, node):
        """namedtuple('Import', ('names',))"""
        return "import {}".format(', '.join(self.write_lines(node.names)))

    def write_ImportFrom(self, node):
        """namedtuple('ImportFrom', ('module', 'names', 'level'))"""
        assert node.level == 0
        return "from {} import {}".format(node.module, ', '.join(self.write_lines(node.names)))

    def write_In(self, node):
        """namedtuple('In', ())"""
        raise NotImplementedError

    def write_Index(self, node):
        """namedtuple('Index', ('value',))"""
        raise NotImplementedError

    def write_Interactive(self, node):
        """namedtuple('Interactive', ('body',))"""
        raise NotImplementedError

    def write_Invert(self, node):
        """namedtuple('Invert', ())"""
        raise NotImplementedError

    def write_Is(self, node):
        """namedtuple('Is', ())"""
        raise NotImplementedError

    def write_IsNot(self, node):
        """namedtuple('IsNot', ())"""
        raise NotImplementedError

    def write_LShift(self, node):
        """namedtuple('LShift', ())"""
        raise NotImplementedError

    def write_Lambda(self, node):
        """namedtuple('Lambda', ('args', 'body'))"""
        raise NotImplementedError

    def write_List(self, node):
        """namedtuple('List', ('elts', 'ctx'))"""
        return "[{}]".format(', '.join(map(str, self.write_lines(node.elts))))

    def write_ListComp(self, node):
        """namedtuple('ListComp', ('elt', 'generators'))"""
        return "[{} {}]".format(
            self.write(node.elt), 
            ' '.join(map(self.write, node.generators))
        )

    def write_Load(self, node):
        """namedtuple('Load', ())"""
        raise NotImplementedError

    def write_Lt(self, node):
        """namedtuple('Lt', ())"""
        return "<"

    def write_LtE(self, node):
        """namedtuple('LtE', ())"""
        return "<="

    def write_Mod(self, node):
        """namedtuple('Mod', ())"""
        return "%"

    def write_Module(self, node):
        """namedtuple('Module', ('body',))"""
        return self.write_lines(node.body)

    def write_Mult(self, node):
        """namedtuple('Mult', ())"""
        return "*"

    def write_Name(self, node):
        """namedtuple('Name', ('id', 'ctx'))"""
        return node.id

    def write_Not(self, node):
        """namedtuple('Not', ())"""
        return "not"

    def write_NotEq(self, node):
        """namedtuple('NotEq', ())"""
        return "!="

    def write_NotIn(self, node):
        """namedtuple('NotIn', ())"""
        return "not in"

    def write_Num(self, node):
        """namedtuple('Num', ('n',))"""
        return str(node.n)

    def write_Or(self, node):
        """namedtuple('Or', ())"""
        return "or"

    def write_Param(self, node):
        """namedtuple('Param', ())"""
        raise NotImplementedError

    def write_Pass(self, node):
        """namedtuple('Pass', ())"""
        return "pass"

    def write_Pow(self, node):
        """namedtuple('Pow', ())"""
        return "*"

    def write_Print(self, node):
        """namedtuple('Print', ('dest', 'values', 'nl'))"""
        assert node.dest == None
        assert node.nl
        return "print {}".format(', '.join(self.write_lines(node.values)))

    def write_RShift(self, node):
        """namedtuple('RShift', ())"""
        return ">>"

    def write_Raise(self, node):
        """namedtuple('Raise', ('type', 'inst', 'tback'))"""
        assert node.inst is None
        assert node.tback is None

        return "raise {}".format(self.write(node.type) if node.type else "")

    def write_Repr(self, node):
        """namedtuple('Repr', ('value',))"""
        raise NotImplementedError

    def write_Return(self, node):
        """namedtuple('Return', ('value',))"""
        return "return {}".format(self.write(node.value))

    def write_Set(self, node):
        """namedtuple('Set', ('elts',))"""
        raise NotImplementedError

    def write_SetComp(self, node):
        """namedtuple('SetComp', ('elt', 'generators'))"""
        raise NotImplementedError

    def write_Slice(self, node):
        """namedtuple('Slice', ('lower', 'upper', 'step'))"""   
        slice_el = lambda n: n if n != "None" and n else ""
        return "[{}]".format(":".join(
                map(
                    slice_el, 
                    map(
                        self.write, 
                        [node.lower, node.upper, node.step]
                    )
                )
            ))

    def write_Store(self, node):
        """namedtuple('Store', ())"""
        raise NotImplementedError

    def write_Str(self, node):
        """namedtuple('Str', ('s',))"""
        return repr(node.s)

    def write_Sub(self, node):
        """namedtuple('Sub', ())"""
        return "-"

    def write_Subscript(self, node):
        """namedtuple('Subscript', ('value', 'slice', 'ctx'))"""
        return "{}{}".format(self.write(node.value), self.write(node.slice))

    def write_Suite(self, node):
        """namedtuple('Suite', ('body',))"""
        raise NotImplementedError

    def write_TryExcept(self, node):
        """namedtuple('TryExcept', ('body', 'handlers', 'orelse'))"""
        raise NotImplementedError

    def write_TryFinally(self, node):
        """namedtuple('TryFinally', ('body', 'finalbody'))"""
        raise NotImplementedError

    def write_Tuple(self, node):
        """namedtuple('Tuple', ('elts', 'ctx'))"""
        return "({})".format(', '.join(map(self.write, node.elts)))

    def write_UAdd(self, node):
        """namedtuple('UAdd', ())"""
        raise NotImplementedError

    def write_USub(self, node):
        """namedtuple('USub', ())"""
        raise NotImplementedError

    def write_UnaryOp(self, node):
        """namedtuple('UnaryOp', ('op', 'operand'))"""
        return "{} {}".format(self.write(node.op), self.write(node.operand))

    def write_While(self, node):
        """namedtuple('While', ('test', 'body', 'orelse'))"""
        raise NotImplementedError

    def write_With(self, node):
        """namedtuple('With', ('context_expr', 'optional_vars', 'body'))"""
        raise NotImplementedError

    def write_Yield(self, node):
        """namedtuple('Yield', ('value',))"""
        raise NotImplementedError

    def write_alias(self, node):
        """namedtuple('alias', ('name', 'asname'))"""
        if node.asname:
            return "{} as {}".format(node.name, node.asname)
        return node.name

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

        return ', '.join(args)

    def write_boolop(self, node):
        """namedtuple('boolop', ())"""
        raise NotImplementedError

    def write_cmpop(self, node):
        """namedtuple('cmpop', ())"""
        raise NotImplementedError

    def write_comprehension(self, node):
        """namedtuple('comprehension', ('target', 'iter', 'ifs'))"""
        r = "for {} in {}".format(self.write(node.target), self.write(node.iter))
        for i in node.ifs:
            r += " if {}".format(self.write(i))
        return r

    def write_excepthandler(self, node):
        """namedtuple('excepthandler', ())"""
        raise NotImplementedError

    def write_expr(self, node):
        """namedtuple('expr', ())"""
        raise NotImplementedError

    def write_expr_context(self, node):
        """namedtuple('expr_context', ())"""
        raise NotImplementedError

    def write_keyword(self, node):
        """namedtuple('keyword', ('arg', 'value'))"""
        raise NotImplementedError

    def write_mod(self, node):
        """namedtuple('mod', ())"""
        raise NotImplementedError

    def write_operator(self, node):
        """namedtuple('operator', ())"""
        raise NotImplementedError

    def write_slice(self, node):
        """namedtuple('slice', ())"""
        raise NotImplementedError

    def write_stmt(self, node):
        """namedtuple('stmt', ())"""
        raise NotImplementedError

    def write_unaryop(self, node):
        """namedtuple('unaryop', ())"""
        raise NotImplementedError