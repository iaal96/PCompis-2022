import ply.lex as lex

#Palabras Reservadas
reserved = {
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'while':'WHILE',
    'do':'DO',
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
t_CST_STRING = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_CST_CHAR =  r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')'

#Ignorados
t_ignore = " \t\r"

#Comentario
t_COMMENT_TEXT = r'%%.*\n'

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


lexer = lex.lex()

f = open('test.txt','r')
program = f.read()
lex.lex()
#lex.input(program)
#while 1:
    #tok = lex.token()
    #if not tok: break
    #print(tok)
#import ply.yacc as yacc

def p_program(t):
    'program : PROGRAM ID SEMICOLON programVars programFunc main'
    print("Code OK")


def p_error(t):
   print("Syntax error: Unexpected token '%s' in line %d" % (t.value, t.lexer.lineno))

def p_main(t):
    'main : MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_programVars(t):
    '''programVars : declaration
                   | '''

def p_programFunc(t):
    '''programFunc : function programFunc
                   | '''

def p_assignment(t):
    'assignment : ID EQUAL expression2 SEMICOLON'

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
    'return : RETURN LEFTPAR expression2 RIGHTPAR'

def p_if(t):
    'if : IF LEFTPAR expression2 RIGHTPAR THEN LEFTBRACE statement RIGHTBRACE ifElse'

def p_ifElse(t):
     '''ifElse : ELSE LEFTBRACE statement RIGHTBRACE
              | '''

def p_for(t):
    'for : FOR forDeclaration TO expression2 DO statement'

def p_forDeclaration(t):
    'forDeclaration : ID EQUAL CST_INT'

def p_comment(t):
    'comment : COMMENT_TEXT'

def p_while(t):
    'while : WHILE LEFTPAR expression2 RIGHTPAR DO statement'

def p_vars(t):
    'vars : ID varsArray varsComa'

def p_varsComa(t):
      '''varsComa : COMA vars
                | '''

def p_varsMatrix(t):
     '''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK
                  | '''

def p_varsArray(t):
    '''varsArray : LEFTBRACK CST_INT RIGHTBRACK varsMatrix
                 | '''

def p_function(t):
     '''function : functionType LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''

def p_param(t):
    'param: PDT ID functionParam'

def p_functionParam(t):
      '''functionParam : COMA param
                     | '''

def p_functionType(t):
     '''functionType : FUNCTION PDT
                    | FUNCTION VOID '''

def cst_PDT(t):
        '''cst_prim : CST_INT
                | CST_FLOAT
                | CST_CHAR '''


def p_Expression2(t):
    '''Expression2 : Expression3 Expression22 Expression3
                       | Expression3 
                       | Expression3 matrixOperator'''

def p_Expression22(t):
    '''Expression22 : AND
                         | OR '''

def p_Expression3(t):
    '''Expression3 : exp Expression33 exp
                       | exp '''

def p_Expression33(t):
    '''Expression33 : GT
                         | LT
                         | NOTEQUAL '''

def p_matrixOperator(t):
    '''matrixOperator : EXCLAMATION
                      | QUESTION
                      | DOLLARSIGN
                      | '''

def p_exp(t):
    '''exp : term expFunction
           | term '''

def p_expFunction(t):
    '''expFunction : PLUS exp
                   | MINUS exp '''



def p_term(t):
        '''term : factor termFunction
            | factor '''

def p_termFunction(t):
        '''termFunction : MULTIPLY term
                    | DIVIDE term '''

def p_factor(t):
    '''factor : LEFTPAR hyperExpression RIGHTPAR
              | cst_prim
              | module
              | ID '''

def p_exp(t):
        '''exp : term expFunction
            | term '''

def p_expFunction(t):
      '''expFunction : PLUS exp
                    | MINUS exp
                    | ''' 

def p_read(t):
    'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
    'id_list : ID id_listFunction'

def p_id_listFunction(t):
        '''id_listFunction : COMA id_list
                    | '''

def p_print(t):
    'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
        '''printFunction : print_param COMA printFunction2
                     | print_param'''

def p_printFunction2(t):
        'printFunction2 : printFunction'

def p_print_param(t):
     '''print_param : expression2
                 | CST_STRING'''

def p_module(t):
     'module : ID LEFTPAR moduleFunction'

def p_statement(t):
     '''statement : return
                 | if 
                 | comment 
                 | read 
                 | print 
                 | assignment 
                 | declaration 
                 | module 
                 | for 
                 | while 
                 | '''


def p_moduleFunction(t):
    '''moduleFunction : ID COMA moduleFunction
                        | ID RIGHTPAR
                        | expression2 COMA moduleFunction
                        | expression2 RIGHTPAR'''


parser = yacc.yacc()

parser.parse(program)