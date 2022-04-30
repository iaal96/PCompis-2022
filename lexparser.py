import ply.lex as lex

#Palabras Reservadas
reserved = {
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'while':'WHILE',
    'do':'DO',
    'from':'FROM',
    'to':'TO',
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
    'GT',
    'LT',
    'AND',
    'OR',
    'LEFTPAR',
    'RIGHTPAR',
    'COMA',
    'EQUAL',
    'COLON',
    'SEMICOLON',
    'ID',
    'PERCENT',
    'LEFTBRACK',
    'RIGHTBRACK',
    'LEFTBRACE',
    'RIGHTBRACE',
    'CST_INT',
    'CST_FLOAT',
    'CST_STRING',
    'CST_CHAR',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MULTIPLY = r'\*'
t_NOTEQUAL = r'<>'
t_GT = r'>'
t_LT = r'<'
t_AND = r'&'
t_OR = r'\|'
t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_COMA = r','
t_EQUAL = r'='
t_COLON = r':'
t_SEMICOLON = r';'
t_PERCENT = r'%'
t_LEFTBRACK = r'\['
t_RIGHTBRACK = r'\]'
t_LEFTBRACE = r'\{'
t_RIGHTBRACE = r'\}'
t_CST_INT = r'[0-9]+'
t_CST_FLOAT = r'[0.9]+\.[0.9]+'
t_CST_STRING = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_CST_CHAR =  r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')'

#Ignorados
t_ignore = " \t\r"

#Comentario
t_COMMENT_TEXT = r'.*\n'

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
    print("Ilegal character '%s' " % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

import ply.yacc as yacc

def p_program(t):
    'program : PROGRAM ID SEMICOLON programVars programFunc main'
    print("Code OK")


def p_error(t):
    print("Syntax error in '%s'" % t.value)

def p_main(t):
    'main : MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_programVars(t):
    '''programVars : vars
                   | '''

def p_programFunc(t):
    '''programFunc : function programFunc
                   | '''

def p_assignment(t):
    'assignment : ID EQUAL exp SEMICOLON'

def p_declaration(t):
    'declaration : VAR declarationPDT'

#PDT=Primitive Data Type
def p_declarationPDT(t):
        '''declarationPDT : primitive vars SEMICOLON declarationPDT
                       | '''

def p_PDT(t):
        '''PDT : INT
                 | FLOAT
                 | CHAR '''

def p_return(t):
    'return : RETURN LEFTPAR exp RIGHTPAR'

def p_if(t):
    'if : IF LEFTPAR exp RIGHTPAR THEN LEFTBRACE statement RIGHTBRACE ifElse'

def p_ifElse(t):
     '''ifElse : ELSE LEFTBRACE statement RIGHTBRACE
              | '''

def p_for(t):
    'for : FOR declaration TO expression DO statement'

def p_comment(t):
    'comment : PERCENT PERCENT COMMENT_TEXT'

def p_while(t):
    'while : WHILE LEFTPAR expression RIGHTPAR DO statement'

def p_vars(t):
    'vars : ID varsArray'

def p_varsComa(t):
      '''varsComa : COMA vars
                | '''

def p_varsMatrix(t):
     '''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK
                  | varsComa '''

def p_varsArray(t):
    '''varsArray : LEFTBRACK CST_INT RIGHTBRACK varsMatrix
                 | varsComa '''

def p_function(t):
     '''function : functionType LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE'''

def p_param(t):
    'param: PDT ID functionParam'

def p_functionParam(t):
      '''functionParam : COMA param
                    | '''

def p_functionType(t):
     '''functionType : FUNCTION PDT
                    | FUNCTION void'''

def cst_PDT(t):
        '''cst_prim : CST_INT
                | CST_DEC
                | CST_CHAR '''

def p_factor(t):
     '''factor: LEFTPAR exp RIGHTPAR
            | cst_PDT
            | module
            | ID'''

def p_term(t):
        '''term : factor termFunction
            | factor '''

def p_termFunction(t):
        '''termFunction : MULTIPLY term
                    | DIVIDE term
                    | ''' 

def p_exp(t):
        '''exp : term expFunction
            | term '''

def p_expFunction(t):
      '''termFunction : PLUS exp
                    | MINUS exp
                    | ''' 

def p_read(t):
    'read : READ LEFTPAR id_list RIGHTPAR'

def p_id_list(t):
    'id_list: ID id_listFunction'

def p_id_listFunction(t):
        '''id_listFunction : COMA id_list
                        | '''

def p_print(t):
    'print: PRINT LEFTPAR printFunction RIGHTPAR'

def p_printFunction(t):
        '''printFunction : print_param COMA printFunction2
                    | print_param '''

def p_printFunction2(t):
        '''printFunction2 : printFunction'''

def p_print_param(t):
     '''print_param : exp
                    | CST_STRING
                    | ID '''

def p_module(t):
     '''module : ID LEFTPAR moduleFunction'''

def p_statementFunction(t):
     '''statementFunction : statement'''

def p_moduleFunction(t):
    '''moduleFunction : ID COMA moduleFunction
                        | ID RIGHTPAR
                        | exp COMA moduleFunction
                        | exp RIGHTPAR'''


parser = yacc.yacc()
