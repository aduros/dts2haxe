from pyparsing import *

# Symbols
LPAR, RPAR, LBRACK, RBRACK, LBRACE, RBRACE, COLON, SEMI, COMMA = map(Suppress, "()[]{}:;,")
QUESTION = Literal("?")
ELLIPSES = Literal("...")

# Keywords
INTERFACE = Keyword("interface").setResultsName("interface")
VAR = Keyword("var").setResultsName("var")
FUNCTION = Keyword("function").setResultsName("function")
DECLARE = Keyword("declare")
EXTENDS = Keyword("extends")

ident = Word(alphas+"_", alphanums+"_").setResultsName("ident")

paramList = Forward()
propertyList = Forward()

namedType = ident
anonymousType = propertyList
type_ = Group(namedType | anonymousType).setResultsName("type")

propertyDef = Group(ident + Optional(QUESTION).setResultsName("optional") + \
        Optional(paramList).setResultsName("params") + COLON + type_)
propertyList << LBRACE + ZeroOrMore(propertyDef + SEMI) + RBRACE

paramDef = Group(Optional(ELLIPSES) + ident + Optional(QUESTION) + COLON + type_)
paramList << LPAR + Group(ZeroOrMore(delimitedList(paramDef, ","))) + RPAR

varDecl = Group(DECLARE + VAR + ident + COLON + type_)
functionDecl = Group(DECLARE + FUNCTION + ident + paramList + COLON + type_)
interfaceDecl = Group(INTERFACE + ident + Group(propertyList).setResultsName("props"))

module = ZeroOrMore(varDecl | functionDecl | interfaceDecl | SEMI)

comment = cStyleComment | ("//" + restOfLine)
module.ignore(comment)

def parseFile (file):
    return module.parseFile(file, True)
