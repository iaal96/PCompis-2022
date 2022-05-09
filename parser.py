import lexer as lexer
import ply.yacc as yacc
from EstructuraDatos import quadruples_main, types, operands, operators, variableTable
from EstructuraDatos import functionDir, temp, currentScope, currentType, semanticCube
from quadruples import *

tokens = lexer.tokens


def p_program(t):
    'program : PROGRAM ID programA1 SEMICOLON programVars programFunc main'
    print("Code OK")
    operands.print()
    types.print()
    operators.print()
    print ("QUADS")
    Quadruples.print_all()
    print ("QUADS MAIN")
    #quadruples_main.print()
    variableTable.clear()

#Global scope
def p_globalTable(t):
    'programA1 : '
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
   exit(0)

def p_main(t):
    'main : mainA1 MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_mainTable(t):
    'mainA1 : '
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
    'assignment : ID EQUAL Expression2 SEMICOLON'
    if t[1] in variableTable[currentScope]:
        if types.pop() == variableTable[currentScope][t[1]]["type"]:
            #quadruples_main.push(("=", operands.pop(), None, t[1]))
            temp_quad = Quadruple("=", operands.pop(), None, t[1])
            Quadruples.push_quad(temp_quad)
        else:
            print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
            exit(0)
    elif t[1] in variableTable["global"]:
        if types.pop() == variableTable["global"][t[1]]["type"]:
            #quadruples_main.push(("=", operands.pop(), None, t[1]))
            temp_quad = Quadruple("=", operands.pop(), None, t[1])
            Quadruples.push_quad(temp_quad)
        else:
            print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
            exit(0)

def p_declaration(t):
    'declaration : VAR declarationPDT'

#PDT=Primitive Data Type
def p_declarationPDT(t):
        '''declarationPDT : PDT vars SEMICOLON declarationPDT
                       | '''

def p_PDT(t):
        '''PDT : INT
                 | FLOAT
                 | CHAR '''
        
# Al indicar tipo, cambiar currentType por declaracion
    #global currentType
    #currentType = t[1]
    

def p_return(t):
    'return : RETURN LEFTPAR Expression2 RIGHTPAR SEMICOLON'

def p_if(t):
    'if : IF LEFTPAR Expression2 RIGHTPAR THEN LEFTBRACE statement RIGHTBRACE ifElse'

def p_ifElse(t):
     '''ifElse : ELSE LEFTBRACE statement RIGHTBRACE
              | '''

def p_for(t):
    'for : FOR forDeclaration TO Expression2 LEFTBRACE statement RIGHTBRACE'

def p_forDeclaration(t):
    'forDeclaration : ID EQUAL CST_INT'

def p_comment(t):
    'comment : COMMENT_TEXT'

def p_while(t):
    'while : WHILE LEFTPAR Expression2 RIGHTPAR LEFTBRACE DO statement RIGHTBRACE'

def p_vars(t):
    'vars : ID varsA1 varsArray varsComa'

def p_addToTable(t):
    'varsA1 : '
    #Si el ID actual existe en scope, lanzar error
    if t[-1] in variableTable[currentScope]:
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
    '''function : functionType ID functionA1 LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType ID functionA1 LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''
    #Resetear scope a global cuando se salga del scope de la funcion, eliminar varTable y referenciar en functionDir
    global currentScope
    #del variableTable[currentScope]
    #del functionDir[currentScope]["vars"]
    currentScope = "global"

def p_param(t):
    'param : PDT ID paramA1 functionParam'

def p_functionParam(t):
      '''functionParam : COMA param
                     | '''

def p_addFuncParams(t):
    'paramA1 : '
    # Si parametro de la funcion ya existe en el scope (o global),dar error
    if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Agregar parametro funcion a variableTable de currentScope
        variableTable[currentScope][t[-1]] = {"type": currentType}

def p_functionType(t):
     '''functionType : FUNCTION PDT
                    | FUNCTION VOID functionTypeA1 '''

def p_cst_PDT(t):
        '''cst_PDT : CST_INT cstprimA1
                | CST_FLOAT cstprimA2
                | CST_CHAR cstprimA3'''
        t[0] = t[1]

def p_addTypeInt(t):
    'cstprimA1 : '
    types.push("int")

def p_addTypeFloat(t):
    'cstprimA2 : '
    types.push("float")

def p_addTypeChar(t):
    'cstprimA3 : '
    types.push("char")

def p_addToDir(t):
    'functionA1 : '
    # Si la funcion ya existe en scope global, lanzar error
    if t[-1] in functionDir["global"] or t[-1] in variableTable["global"]:
        print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        global currentScope
        global currentType
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
    '''Expression2 : Expression3 Exp2A1 Expression22 Expression2Nested
                       | Expression3 opMatrix 
                       | Expression3 Exp2A1'''

def p_Expression2Nested(t):
    '''Expression2Nested : Expression3 Exp2A1 Expression22 Expression2Nested
                             | Expression3 Exp2A1'''


def p_opConsumeExp2(t):
    'Exp2A1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == "|" or operators.peek() == "&":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                #quadruples_main.push((oper, lOp, rOp, "t%d"%temp))
                temp_quad = Quadruple(oper, lOp, rOp, "t"+str(temp))
                Quadruples.push_quad(temp_quad)
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_Expression22(t):
    '''Expression22 : AND addOperator
                    | OR addOperator'''

def p_Expression3(t):
    '''Expression3 : exp Exp3A1 Expression33 exp Exp3A1
                       | exp Exp3A1'''

def p_Expression33(t):
    '''Expression33 : GT addOperator
                    | LT addOperator
                    | NOTEQUAL addOperator
                    | ISEQUAL addOperator'''

def p_opConsumeExp3(t):
    'Exp3A1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek == "==":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                #quadruples_original.push((oper, lOp, rOp, "t%d"%temp))
                temp_quad = Quadruple(oper, lOp, rOp, "t"+str(temp))
                Quadruples.push_quad(temp_quad)
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_opMatrix(t):
    '''opMatrix : EXCLAMATION addOperator
                | QUESTION addOperator
                | DOLLARSIGN addOperator'''

def p_exp(t):
    '''exp : term termA1 expFunction
           | term termA1'''

def p_opConsumeExp(t):
    'termA1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == "+" or operators.peek() == "-":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                #quadruples_main.push((oper, lOp, rOp, "t%d"%temp))
                temp_quad = Quadruple(oper, lOp, rOp, "t"+str(temp))
                Quadruples.push_quad(temp_quad)
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_expFunction(t):
    '''expFunction : PLUS addOperator exp
                   | MINUS addOperator exp '''

def p_setVoid(t):
    'functionTypeA1 : '
    # Establecer void como currentType
    global currentType
    currentType = t[-1]

def p_term(t):
        '''term : factor factorA1 termFunction
            | factor factorA1'''

def p_opConsumeTerm(t):
    'factorA1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == "*" or operators.peek() == "/":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                #quadruples_main.push((oper, lOp, rOp, "t%d"%temp))
                temp_quad = Quadruple(oper, lOp, rOp, "t"+str(temp))
                Quadruples.push_quad(temp_quad)
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_termFunction(t):
        '''termFunction : MULTIPLY addOperator term
                    | DIVIDE addOperator term '''

def p_addOperator(t):
    'addOperator : '
    operators.push(t[-1])

def p_factor(t):
    '''factor : LEFTPAR Expression2 RIGHTPAR
              | cst_PDT addOperand
              | module
              | ID addOperand addTypeId '''

def p_addOperand(t):
    'addOperand : '
    operands.push(t[-1])

def p_addTypeId(t):
    'addTypeId : '
    if t[-2] in variableTable[currentScope]:
        types.push(variableTable[currentScope][t[-2]]["type"])
    elif t[-2] in variableTable["global"]:
        types.push(variableTable["global"][t[-2]]["type"])
    else:
        print("Error: undefined '%s' used in line %d" % (t[-1], t.lexer.lineno))


def p_read(t):
    'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
    'id_list : ID addRead id_listFunction'

def p_id_listFunction(t):
        '''id_listFunction : COMA id_list
                    | '''

def p_addRead(t):
    'addRead : '
    if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
        #quadruples_main.push(("read", None, None, t[-1]))
        temp_quad = Quadruple("read", None, None, t[-1])
        Quadruples.push_quad(temp_quad)
    else:
        print("Error: undefined '%s' used in line %d" % (t[-1], t.lexer.lineno))

def p_print(t):
    'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
        '''printFunction : print_param COMA printFunction2
                     | print_param '''

def p_printFunction2(t):
        'printFunction2 : printFunction'

def p_addPrint(t):
    'addPrint : '
    #quadruples_main.push(("print", None, None, operands.pop()))
    temp_quad = Quadruple("print", None, None, operands.pop())
    Quadruples.push_quad(temp_quad)
    types.pop()


def p_print_param(t):
     '''print_param : Expression2 addPrint
                 | CST_STRING addPrintString'''

def p_addPrintString(t):
    'addPrintString : '
    #quadruples_main.push(("print", None, None, t[-1]))
    temp_quad = Quadruple("print", None, None, t[-1])
    Quadruples.push_quad(temp_quad)

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
                        | Expression2 COMA moduleFunction
                        | Expression2 RIGHTPAR
                        | '''

import sys


if len(sys.argv) > 1:
	f = open(sys.argv[1], "r")
else:
	f = open("prog.txt", "r")
program = f.read()

parser = yacc.yacc()

parser.parse(program)