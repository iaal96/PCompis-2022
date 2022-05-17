import ply.lex as lex

#Palabras Reservadas
reserved = {
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'while':'WHILE',
    'to':'TO',
    'for':'FOR',
    'program':'PROGRAM',
    'main':'MAIN',
    'var':'VAR',
    'void':'VOID',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
    'return':'RETURN',
    'read':'READ',
    'print':'PRINT',
    'function':'FUNCTION'
}

#Tokens
tokens = [
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'NOTEQUAL',
    'ISEQUAL',
    'GT',
    'LT',
    'AND',
    'OR',
    'LEFTPAR',
    'RIGHTPAR',
    'COMA',
    'EQUAL',
    'SEMICOLON',
    'ID',
    'EXCLAMATION',
    'QUESTION',
    'DOLLARSIGN',
    'LEFTBRACK',
    'RIGHTBRACK',
    'LEFTBRACE',
    'RIGHTBRACE',
    'CST_INT',
    'CST_FLOAT',
    'CST_STRING',
    'CST_CHAR',
    'COMMENT_TEXT'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MULTIPLY = r'\*'
t_NOTEQUAL = r'<>'
t_ISEQUAL = r'=='
t_GT = r'>'
t_LT = r'<'
t_AND = r'&'
t_OR = r'\|'
t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_COMA = r','
t_EQUAL = r'='
t_SEMICOLON = r';'
t_LEFTBRACK = r'\['
t_EXCLAMATION = r'!'
t_QUESTION = r'\?'
t_DOLLARSIGN = r'\$'
t_RIGHTBRACK = r'\]'
t_LEFTBRACE = r'\{'
t_RIGHTBRACE = r'\}'
t_CST_INT = r'[0-9]+'
t_CST_FLOAT = r'[0.9]+\.[0.9]+'
t_CST_STRING    = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_COMMENT_TEXT =  r'%%.*\n'

#Ignorados
t_ignore = " \t\r"

#ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

#Salto de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


#Error
def t_error(t):
    print("Illegal character '%s' in line %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    exit(0)

def t_CST_CHAR(t):
    r'\'[a-zA-Z]\''
    t.value = t.value
    return t

lexer = lex.lex(errorlog=lex.NullLogger())
print("Lexer generado.")
    
lex.lex()