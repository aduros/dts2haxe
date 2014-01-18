class Class ():
    interface = None
    var = None

def render (program):
    output = []

    indent_stack = []
    def begin_indent():
        indent_stack.append("\t")
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

    def w_type (type):
        if type.ident:
            w_ident(type.ident)
        else:
            w_anonymous_type(type)

    def w_anonymous_type (type):
        w("{")
        for ii, prop in enumerate(type):
            if ii > 0:
                w(" ")
            w_property(prop)
        w("}")

    def w_property (prop):
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
        w_type(prop.type)
        w(";")

    def w_param (param):
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
        w("class ")
        w(ident)
        wln(" {")
        begin_indent()
        if cl.interface:
            for prop in cl.interface.props:
                w_property(prop)
                wln()
        if cl.var:
            for prop in cl.var.type:
                w("static ")
                w_property(prop)
                wln()
        end_indent()
        wln("}")

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
