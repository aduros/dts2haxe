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

    def w_type (type, ignore_array=False):
        if type.ident:
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
        elif type.arrow:
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
        else:
            w_anonymous_type(type)

    def w_anonymous_type (type):
        wln("{")
        begin_indent()
        for ii, prop in enumerate(type):
            if ii > 0:
                wln()
            w_property(prop)
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
        w(";")

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
            w_type(param.type)

    def w_params (params):
        w("(")
        for ii, param in enumerate(params):
            if ii > 0:
                w(", ")
            w_param(param)
        w(")")

    def w_extends (type):
        if type.extends:
            w(" extends ")
            w_ident(type.extends.ident)
        if type.implements:
            wln()
            begin_indent()
            for ii, iface in enumerate(type.implements):
                if ii > 0:
                    wln()
                w("implements ")
                w_ident(iface)
            end_indent()

    def w_class (ident, cl):
        wln("@:native(\"%s\")" % ident)
        w("extern class ")
        w_ident(ident)
        if cl.interface:
            w_extends(cl.interface)
        if cl.tsclass:
            w_extends(cl.tsclass)
        wln()
        wln("{")
        begin_indent()
        if cl.interface:
            for prop in cl.interface.props:
                w_property(prop)
                wln()
        if cl.var:
            for prop in cl.var.type:
                w_property(prop, "static " if prop.ident != "new" else None)
                wln()
        if cl.tsclass:
            for prop in cl.tsclass.props:
                w_property(prop)
                wln()
        end_indent()
        wln("}")

    # Combine interface and var declaration into single classes
    classes = {}
    for statement in program:
        cl = classes.get(statement.ident)
        if not cl:
            cl = classes[statement.ident] = HaxeClass()
        if statement.interface:
            cl.interface = statement
        elif statement.var:
            cl.var = statement
        elif statement.tsclass:
            cl.tsclass = statement

    for ident, cl in classes.iteritems():
        w_class(ident, cl)
        wln()
    return "".join(output)
