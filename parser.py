from pyparsing import *

# Symbols
LPAR, RPAR, LBRACK, RBRACK, LBRACE, RBRACE, COLON, SEMI, COMMA, EQUALS = map(Suppress, "()[]{}:;,=")
QUESTION = Literal("?").setResultsName("optional")
ELLIPSES = Literal("...").setResultsName("varargs")
ARROW = Literal("=>").setResultsName("arrow")

# Keywords
def kwd (name):
    return Keyword(name).setResultsName(name)
CLASS = kwd("class").setResultsName("tsclass")
CONSTRUCTOR = kwd("constructor")
DECLARE = Optional(kwd("declare"))
ENUM = kwd("enum")
EXPORT = kwd("export")
EXTENDS = kwd("extends")
FUNCTION = kwd("function")
IMPLEMENTS = kwd("implements")
INTERFACE = kwd("interface")
MODULE = kwd("module")
STATIC = kwd("static")
VAR = kwd("var")

ident = Word(alphas+"_$", alphanums+"_$.").setResultsName("ident")

paramList = Forward()
propertyList = Forward()
type_ = Forward()
typeDecl = Forward()

# Types
namedType = ident
anonymousType = propertyList
functionType = paramList.setResultsName("params") + ARROW + type_
type_ << Group((namedType | anonymousType | functionType) + ZeroOrMore(Group(LBRACK + RBRACK)).setResultsName("array")).setResultsName("type")

# Properties
field = ident + Optional(QUESTION) + Optional(paramList).setResultsName("params")
invokeAccess = Group(paramList).setResultsName("invoke")
dictionaryAccess = LBRACK + ident + COLON + Group(type_).setResultsName("dictionary") + RBRACK
constructor = CONSTRUCTOR + paramList.setResultsName("params")
propertyAttribs = ZeroOrMore(STATIC)
propertyDef = Group(propertyAttribs + (constructor | field | invokeAccess | dictionaryAccess) + Optional(COLON + type_))
propertyList << LBRACE + ZeroOrMore(propertyDef + SEMI).setResultsName("props") + RBRACE

# Parameters
optional = ident + QUESTION + COLON + type_
varargs = ELLIPSES + ident + COLON + type_
argument = Optional(ident + COLON) + type_
paramDef = Group(optional | argument | varargs)
paramList << LPAR + Group(ZeroOrMore(delimitedList(paramDef, ","))) + RPAR

varDecl = Group(DECLARE + VAR - ident + COLON + type_)
functionDecl = Group(DECLARE + FUNCTION - ident + paramList.setResultsName("params") + COLON + type_)

extends = Group(Optional(EXTENDS + delimitedList(ident, ","))).setResultsName("extends")
implements = Optional(IMPLEMENTS + Group(delimitedList(ident, ",")).setResultsName("implements"))
interfaceDecl = Group(INTERFACE + ident - extends + Group(propertyList).setResultsName("props"))
classDecl = Group(CLASS + ident - extends - implements + Group(propertyList).setResultsName("props"))
enumValue = Group(ident + Optional(EQUALS + Word(nums)))
enumDecl = Group(ENUM + ident + LBRACE + ZeroOrMore(delimitedList(enumValue, ",")).setResultsName("vals") + Optional(COMMA) + RBRACE)
moduleDecl = Group(DECLARE + MODULE + ident + LBRACE + ZeroOrMore(typeDecl).setResultsName("entries") + RBRACE)
typeDecl << Suppress(ZeroOrMore(EXPORT)) + (varDecl | functionDecl | interfaceDecl | classDecl | enumDecl | moduleDecl) + ZeroOrMore(SEMI)

program = ZeroOrMore(moduleDecl | typeDecl | SEMI)
program.ignore(cppStyleComment)
program.ignore(Regex(r"<.*?>"))

def parseFile (file):
    return program.parseFile(file, True)
