from pyparsing import *

# Symbols
LPAR, RPAR, LBRACK, RBRACK, LBRACE, RBRACE, COLON, SEMI, COMMA = map(Suppress, "()[]{}:;,")
QUESTION = Literal("?").setResultsName("optional")
ELLIPSES = Literal("...").setResultsName("varargs")
ARROW = Literal("=>").setResultsName("arrow")

# Keywords
def kwd (name):
    return Keyword(name).setResultsName(name)
INTERFACE = kwd("interface")
VAR = kwd("var")
FUNCTION = kwd("function")
CLASS = kwd("class").setResultsName("tsclass")
STATIC = kwd("static")
DECLARE = kwd("declare")
EXTENDS = kwd("extends")
IMPLEMENTS = kwd("implements")
EXPORT = kwd("export")

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
propertyAttribs = ZeroOrMore(STATIC)
propertyDef = Group(propertyAttribs + (field | applyMethod | arrayAccess) + COLON + type_)
propertyList << LBRACE + ZeroOrMore(propertyDef + SEMI) + RBRACE

# Parameters
argument = Optional(ident + COLON) + type_
optional = ident + QUESTION + COLON + type_
varargs = ELLIPSES + ident + COLON + type_
paramDef = Group(argument | optional | varargs)
paramList << LPAR + Group(ZeroOrMore(delimitedList(paramDef, ","))) + RPAR

varDecl = Group(DECLARE + VAR - ident + COLON + type_)
functionDecl = Group(DECLARE + FUNCTION - ident + paramList + COLON + type_)

extends = Group(Optional(EXTENDS + delimitedList(ident, ","))).setResultsName("extends")
implements = Optional(IMPLEMENTS + Group(delimitedList(ident, ",")).setResultsName("implements"))
interfaceDecl = Group(INTERFACE + ident - extends + Group(propertyList).setResultsName("props"))
classDecl = Group(CLASS + ident - extends - implements + Group(propertyList).setResultsName("props"))
typeDecl = ZeroOrMore(EXPORT) + (varDecl | functionDecl | interfaceDecl | classDecl)

module = ZeroOrMore(typeDecl + ZeroOrMore(SEMI))
module.ignore(cppStyleComment)
module.ignore(Regex(r"<.*?>"))

def parseFile (file):
    return module.parseFile(file, True)
