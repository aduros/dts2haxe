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

class Class ():
    interface = None
    var = None

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

    def w_type (type):
        if type.ident:
            haxe_type = haxe_types.get(type.ident, type.ident).capitalize()
            if type.array != "":
                w("Array<")
                w(haxe_type)
                w(">")
            else:
                w(haxe_type)
        elif type.arrow:
            for ii, param in enumerate(type.params):
                if ii > 0:
                    w(" -> ")
                if param.optional:
                    w("?")
                w_type(param.type)
        else:
            w_anonymous_type(type)

    def w_anonymous_type (type):
        w("{")
        for ii, prop in enumerate(type):
            if ii > 0:
                w(" ")
            w_property(prop)
        w("}")

    def w_property (prop, attributes=None):
        if prop.ident in haxe_keywords:
            wln("@:native(\"%s\")" % prop.ident)
        if attributes:
            w(attributes)

        method = prop.params != ""
        if method:
            w("function ")
            w_ident(prop.ident)
            w(" ")
            w_params(prop.params)
        else:
            w("var ")
            w_ident(prop.ident)
            if prop.optional:
                w("?")

        w(" :")
        if prop.ident == "new":
            w("Void")
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
                w_type(param.type)
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

    def w_class (ident, cl):
        wln("@:native(\"%s\")" % ident)
        w("extern class ")
        w_ident(ident)
        if cl.interface and cl.interface.extends:
            w(" extends ")
            w_ident(cl.interface.extends.ident)
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
        end_indent()
        wln("}")

    # Combine interface and var declaration into single classes
    classes = {}
    for statement in program:
        cl = classes.get(statement.ident)
        if not cl:
            cl = classes[statement.ident] = Class()
        if statement.interface:
            cl.interface = statement
        elif statement.var:
            cl.var = statement

    for ident, cl in classes.iteritems():
        w_class(ident, cl)
        wln()
    return "".join(output)
