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

ident = Word(alphas+"_$", alphanums+"_$.").setResultsName("ident")

paramList = Forward()
propertyList = Forward()
type_ = Forward()

# Types
namedType = ident + ZeroOrMore(Group(LBRACK + RBRACK)).setResultsName("array")
anonymousType = propertyList
functionType = paramList.setResultsName("params") + ARROW + type_
type_ << Group(namedType | anonymousType | functionType).setResultsName("type")

# Properties
field = ident + Optional(QUESTION) + Optional(paramList).setResultsName("params")
applyMethod = paramList
arrayAccess = LBRACK + Suppress(ident) + COLON + type_ + RBRACK
propertyDef = Group((field | applyMethod | arrayAccess) + COLON + type_)
propertyList << LBRACE + ZeroOrMore(propertyDef + SEMI) + RBRACE

# Parameters
argument = Optional(ident + COLON) + type_
optional = ident + QUESTION + COLON + type_
varargs = ELLIPSES + ident + COLON + type_
paramDef = Group(argument | optional | varargs)
paramList << LPAR + Group(ZeroOrMore(delimitedList(paramDef, ","))) + RPAR

varDecl = Group(DECLARE + VAR - ident + COLON + type_)
functionDecl = Group(DECLARE + FUNCTION - ident + paramList + COLON + type_)
interfaceDecl = Group(INTERFACE + ident - Group(Optional(EXTENDS + delimitedList(ident, ","))).setResultsName("extends") + Group(propertyList).setResultsName("props"))

module = ZeroOrMore(varDecl | functionDecl | interfaceDecl | SEMI)
module.ignore(cppStyleComment)
module.ignore(Regex(r"<.*?>"))

def parseFile (file):
    return module.parseFile(file, True)
