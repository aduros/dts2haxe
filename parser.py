from pyparsing import *

# Symbols
LPAR, RPAR, LBRACK, RBRACK, LBRACE, RBRACE, COLON, SEMI, COMMA = map(Suppress, "()[]{}:;,")
QUESTION = Literal("?").setResultsName("optional")
ELLIPSES = Literal("...").setResultsName("varargs")
ARROW = Literal("=>").setResultsName("arrow")

# Keywords
INTERFACE = Keyword("interface").setResultsName("interface")
VAR = Keyword("var").setResultsName("var")
FUNCTION = Keyword("function").setResultsName("function")
DECLARE = Keyword("declare")
EXTENDS = Keyword("extends")

ident = Word(alphas+"_", alphanums+"_").setResultsName("ident")

paramList = Forward()
propertyList = Forward()
type_ = Forward()

namedType = ident + Optional(LBRACK + RBRACK).setResultsName("array")
anonymousType = propertyList
functionType = paramList.setResultsName("params") + ARROW + type_
type_ << Group(namedType | anonymousType | functionType).setResultsName("type")

propertyDef = Group(ident + Optional(QUESTION) + Optional(paramList).setResultsName("params") + COLON + type_)
propertyList << LBRACE + ZeroOrMore(propertyDef + SEMI) + RBRACE

paramDef = Group(Optional(ELLIPSES) + ident + Optional(QUESTION) + COLON + type_)
paramList << LPAR + Group(ZeroOrMore(delimitedList(paramDef, ","))) + RPAR

varDecl = Group(DECLARE + VAR + ident + COLON + type_)
functionDecl = Group(DECLARE + FUNCTION + ident + paramList + COLON + type_)
interfaceDecl = Group(INTERFACE + ident + Group(Optional(EXTENDS + ident)).setResultsName("extends") + Group(propertyList).setResultsName("props"))

module = ZeroOrMore(varDecl | functionDecl | interfaceDecl | SEMI)

comment = cStyleComment | ("//" + restOfLine)
module.ignore(comment)

def parseFile (file):
    return module.parseFile(file, True)
