import pyparsing

haxe_types = {
    "any": "Dynamic",
    "number": "Float",
}

haxe_keywords = set([
    "break", "callback", "case", "cast", "catch", "class", "continue", "default", "do", "dynamic",
    "else", "enum", "extends", "extern", "false", "for", "function", "if", "implements", "import",
    "in", "inline", "interface", "never", "null", "override", "package", "private", "public",
    "return", "static", "super", "switch", "this", "throw", "true", "try", "typedef", "untyped",
    "using", "var", "while",
])

class HaxeClass ():
    interface = None
    var = None
    tsclass = None

def render (program):
    output = []

    indent_stack = []
    def begin_indent():
        indent_stack.append("    ")
    def end_indent():
        indent_stack.pop()

    package_stack = []
    def begin_package(name):
        package_stack.append(name)
    def end_package():
        package_stack.pop()

    def w (text):
        if output and output[-1].endswith("\n"):
            output.extend(indent_stack)
        output.append(text)

    def wln (text=None):
        if text:
            w(text)
        output.append("\n")

    def w_ident (ident):
        w(ident)
        if ident in haxe_keywords:
            w("_")

    def w_func (type):
        if len(type.params) == 0:
            w("Void")
        else:
            for ii, param in enumerate(type.params):
                if ii > 0:
                    w(" -> ")
                if param.optional:
                    w("?")
                w_type(param.type)
        w(" -> ")
        w_type(type.type)

    def w_type (type, ignore_array=False):
        if type.params != "":
            w_func(type)
        elif type.ident:
            haxe_type = haxe_types.get(type.ident, type.ident)
            haxe_type = haxe_type[0].upper() + haxe_type[1:]
            if type.array != "":
                depth = len(type.array)
                if ignore_array:
                    depth -= 1
                w("Array<" * depth)
                w(haxe_type)
                w(">" * depth)
            else:
                w(haxe_type)
        else:
            w_anonymous_type(type)

    def w_anonymous_type (type):
        wln("{")
        begin_indent()
        for ii, prop in enumerate(type):
            if ii > 0:
                wln(",")
            w_param(prop)
        wln()
        end_indent()
        w("}")

    def w_property (prop, attributes=None):
        if prop.ident == "":
            w("// UNSUPPORTED: ")

        if prop.ident in haxe_keywords:
            wln("@:native(\"%s\")" % prop.ident)
        if attributes:
            w(attributes)
        if prop.static:
            w("static ")

        method = prop.params != ""
        if method:
            w("function ")
            w_ident(prop.ident)
            w(" ")
            w_params(prop.params)
        else:
            w("var ")
            w_ident(prop.ident)

        w(" :")
        if prop.ident == "new":
            w("Void")
        else:
            if prop.optional:
                w("Null<")
                w_type(prop.type)
                w(">")
            else:
                w_type(prop.type)

    def w_param (param):
        if param.varargs:
            for ii in range(1, 10):
                if ii > 1:
                    w(", ")
                w("?")
                w_ident(param.ident+str(ii))
                w(" :")
                w_type(param.type, ignore_array=True)
        else:
            if param.optional:
                w("?")
            w_ident(param.ident)
            w(" :")
            w_type(param)

    def w_params (params):
        w("(")
        for ii, param in enumerate(params):
            if ii > 0:
                w(", ")
            w_param(param)
        w(")")

    def escape_package (package):
        package = package.lower();
        if package in haxe_keywords:
            package += "_"
        return package;

    def w_package ():
        if package_stack:
            w("package ")
            for ii, package in enumerate(package_stack):
                if ii > 0:
                    w(".")
                w(escape_package(package))
            wln(";")
            wln()

    def w_native (ident):
        if package_stack:
            wln("@:native(\"%s\")" % ".".join(package_stack + [ident]))

    def w_class (cl):
        w_native(cl.ident)
        if cl.tsclass:
            w("extern class ")
            w_ident(cl.ident)
            if cl.extends:
                w(" extends ")
                w_ident(cl.extends.ident)
            if cl.implements:
                wln()
                begin_indent()
                for ii, iface in enumerate(cl.implements):
                    if ii > 0:
                        wln()
                    w("implements ")
                    w_ident(iface)
                end_indent()
            wln()
            wln("{")
            begin_indent()
            for ii, prop in enumerate(cl.props):
                w_property(prop)
                wln(";")
            end_indent()
            w("}")

        else:
            w("typedef ")
            w_ident(cl.ident)
            wln(" = {")
            begin_indent()
            for ii, prop in enumerate(cl.props):
                w_param(prop)
                wln(",")
            end_indent()
            w("}")

    def w_module (module):
        global_vars = []
        for statement in module:
            if statement.module:
                begin_package(statement.ident)
                w_module(statement.entries)
                end_package()
            else:
                if statement.var:
                    global_vars.append(statement)
                else:
                    w_package()
                    w_class(statement)
                    wln()

        if global_vars:
            w_package()
            if package_stack:
                wln("@:native(\"%s\")" % ".".join(package_stack))
            wln("extern class Globals")
            wln("{")
            begin_indent()
            for var in global_vars:
                w_property(var, "static ")
                wln(";")
            end_indent()
            w("}")

    w_module(program)
    return "".join(output)
