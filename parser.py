import lexer as lexer
import ply.yacc as yacc

tokens = lexer.tokens

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
    'return : RETURN LEFTPAR expression2 RIGHTPAR SEMICOLON'

def p_if(t):
    'if : IF LEFTPAR expression2 RIGHTPAR THEN LEFTBRACE statement RIGHTBRACE ifElse'

def p_ifElse(t):
     '''ifElse : ELSE LEFTBRACE statement RIGHTBRACE
              | '''

def p_for(t):
    'for : FOR forDeclaration TO expression2 LEFTBRACE statement RIGHTBRACE'

def p_forDeclaration(t):
    'forDeclaration : ID EQUAL CST_INT'

def p_comment(t):
    'comment : COMMENT_TEXT'

def p_while(t):
    'while : WHILE LEFTPAR expression2 RIGHTPAR LEFTBRACE DO statement RIGHTBRACE'

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
     '''function : functionType ID LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType ID LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''

def p_param(t):
    'param: PDT ID functionParam'

def p_functionParam(t):
      '''functionParam : COMA param
                     | '''

def p_functionType(t):
     '''functionType : FUNCTION PDT
                    | FUNCTION VOID '''

def cst_PDT(t):
        '''cst_PDT : CST_INT
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
     'module : ID LEFTPAR moduleFunction RIGHTPAR SEMICOLON'

def p_statement(t):
     '''statement : return
                 | if statement
                 | comment statement
                 | read statement
                 | print statement
                 | assignment statement
                 | declaration statement
                 | module statement
                 | for statement
                 | while statement
                 | '''


def p_moduleFunction(t):
    '''moduleFunction : ID COMA moduleFunction
                        | expression2 COMA moduleFunction
                        | expression2 RIGHTPAR
                        | '''

f = open('test.txt','r')
program = f.read()
parser = yacc.yacc()

parser = parse(program)