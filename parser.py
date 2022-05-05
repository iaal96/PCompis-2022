import lexer as lexer
import ply.yacc as yacc

tokens = lexer.tokens

functionDir = {}
currentScope = ""
currentType = "program"
variableTable = {}
'''
    "global": {
        "type": "void",
        "vars": variableTable["global"] -> "i": {
                                                "type": "int"
                                                "value": 1
                                            }
                                            ...
    }

    "main": {
        "type": "void",
        "vars": variableTable["main"] -> "c": {
                                              "type": "char"
                                              "value": "h"
                                         }
                                         ...
    }
'''

def p_program(t):
    'program : PROGRAM ID globalTable SEMICOLON programVars programFunc main'
    print("Code OK")
    print()
    for i in functionDir:
        print("\tfunction name: %s" % i)
        print("\t\ttype: %s" % functionDir[i]["type"])
        print("\t\tvars: %s" % functionDir[i]["vars"])
        print()
    variableTable.clear()

def p_progVT(t):
    'globalTable : '
    #currentScope es global por default
    global currentScope
    currentScope = "global"
    #Inicializar variableTable para global y establecer nombre y tipo a program
    variableTable[currentScope] = {}
    variableTable[currentScope][t[-1]] = {"type": "program"}
    #Inicializar functionDir para global scope
    functionDir[currentScope] = {}
    #Establecer tipo y vars como referencia a variableTable[global]
    functionDir[currentScope]["type"] = "void"
    functionDir[currentScope]["vars"] = variableTable[currentScope]
    


def p_error(t):
   print("Syntax error: Unexpected token '%s' in line %d" % (t.value, t.lexer.lineno))

def p_main(t):
    'main : mainScope MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_mainScope(t):
    'mainScope : '
    global currentScope
    variableTable[currentScope]["main"] = {"type": "void"}
    currentScope = "main"
    # Inicializar variableTable y functionDir para main scope
    variableTable[currentScope] = {}
    functionDir[currentScope] = {}
    # Establecer tipo de funcion y vars como referencia a variableTable["main"]
    functionDir[currentScope]["type"] = "void"
    functionDir[currentScope]["vars"] = variableTable[currentScope]

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
        
# Al indicar tipo, cambiar currentType por declaracion
    global currentType
    currentType = t[1]

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
    'vars : ID addtoTable varsArray varsComa'

def p_addToTable(t):
    'addToTable : '
    #Si el ID actual existe en scope, lanzar error
    if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Agrega ID actual a variableTable[scope]
        variableTable[currentScope][t[-1]] = {"type": currentType}

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
    '''function : functionType ID addToDir LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType ID addToDir LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''
    #Resetear scope a global cuando se salga del scope de la funcion, eliminar varTable y referenciar en functionDir
    global currentScope
    #del variableTable[currentScope]
    #del functionDir[currentScope]["vars"]
    currentScope = "global"

def p_param(t):
    'param: PDT ID addFuncParams functionParam'

def p_functionParam(t):
      '''functionParam : COMA param
                     | '''

def p_addFuncParams(t):
    'addFuncParams : '
    # Si parametro de la funcion ya existe en el scope (o global),dar error
    if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Agregar parametro funcion a variableTable de currentScope
        variableTable[currentScope][t[-1]] = {"type": currentType}

def p_functionType(t):
     '''functionType : FUNCTION PDT
                    | FUNCTION VOID '''

def cst_PDT(t):
        '''cst_PDT : CST_INT
                | CST_FLOAT
                | CST_CHAR '''

def p_addToDir(t):
    'addToDir : '
    global currentScope
    # Si la funcion ya existe en scope global, lanzar error
    if t[-1] in functionDir["global"] or t[-1] in variableTable["global"]:
        print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Agregar funcion a variableTable de currentScope
        variableTable[currentScope][t[-1]] = {"type": currentType}
        # Cambiar scope a nuevo id de la funcion
        currentScope = t[-1]
        # Inicializar variableTable y functionDir para nuevo id de la funcion
        variableTable[currentScope] = {}
        functionDir[currentScope] = {}
        # Establecer nuevo tipo de funcion y vars como referencia a variableTable[currentScope]
        functionDir[currentScope]["type"] = currentType
        functionDir[currentScope]["vars"] = variableTable[currentScope]

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

def p_setVoid(t):
    'setVoid : '
    # Establecer void como currentType
    global currentType
    currentType = t[-1]

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