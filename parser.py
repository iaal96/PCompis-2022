import lexer as lexer
import ply.yacc as yacc
from EstructuraDatos import types, operands, operators, variableTable
from EstructuraDatos import functionDir, temp, currentScope, currentType, semanticCube
from quadruples import *

tokens = lexer.tokens


def p_program(t):
	'program : PROGRAM ID programA1 SEMICOLON programVars programFunc main'
	print("Code ok")
	# show variable table and function directory
	# print()
	# for i in functionDir:
	#	 print("\tfunction name: %s" % i)
	#	 print("\t\ttype: %s" % functionDir[i]["type"])
	#	 print("\t\tvars: %s" % functionDir[i]["vars"])
	#	 print()

	operands.print()
	types.print()
	operators.print()
	print ("QUADS")
	Quadruples.print_all()
	print ("MAIN QUADS")
	variableTable.clear()

#Global scope
def p_globalTable(t):
	'programA1 : '
	# Inicializar variableTable para global scope y definir nombre y tipo del programa
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Inicializar functionDir para global scope
	functionDir[currentScope] = {}
	# Definir tipo y variables como referencia a variableTable["global"]
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
	# Definir tipo de funcion y variables como referencia a variableTable["main"]
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
			temp_quad = Quadruple("=", operands.pop(), None, t[1])
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = t[3]
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
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
	# Cambiar currentType por declaracion
	global currentType
	currentType = t[1]
    

def p_return(t):
	'return : RETURN LEFTPAR Expression2 RIGHTPAR SEMICOLON'

def p_if(t):
	'if : IF LEFTPAR Expression2 RIGHTPAR createJQif THEN LEFTBRACE statement RIGHTBRACE ifElse updateJQ'

#Jump Quad if
def p_createJQif(t):
	'createJQif : '
	result_type = types.pop()
	if result_type == "int":
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			temp_quad = Quadruple(operator, res, None, None)
			Quadruples.push(temp_quad)
			Quadruples.push_jump(-1)
			Quadruples.jump_stack.print()
		else: 
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else: 
		print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)	   

def p_updateJQ(t):
	'updateJQ : '
	Quadruples.jump_stack.print()
	tmp_end = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	tmp_quad = Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_ifElse(t):
	'''ifElse : ELSE createJQelse LEFTBRACE statement RIGHTBRACE
			  | '''

#Jump Quad else
def p_createJQelse(t):
	'createJQelse : '
	operator = "GOTO"
	tmp_quad = Quadruple(operator, None, None, None)
	Quadruples.push_quad(tmp_quad)

	tmp_false = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	tmp_quad = Quadruples.update_jump_quad(tmp_false, tmp_count)
	Quadruples.push_jump(-1)

def p_for(t):
	'for : FOR forDeclaration TO Expression2 LEFTBRACE statement RIGHTBRACE'

def p_forDeclaration(t):
	'forDeclaration : ID EQUAL CST_INT'

def p_comment(t):
	'comment : COMMENT_TEXT'

def p_while(t):
	'while : WHILE LEFTPAR Expression2 RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_vars(t):
	'vars : ID varsA1 varsArray varsComa'

def p_addToTable(t):
	'varsA1 : '
	#Si el ID ya existe en el scope o global, dar error
	if t[-1] in variableTable[currentScope]:
		print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
		exit(0)
	else:
		# Agregar ID actual a variableTable(scope)
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
					| FUNCTION VOID functionTypeA1'''

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
				result = 0
				if operators.peek() == "|": 
					result = lOp or rOp
				else: 
					result = lOp and rOp
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
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
				result = 0
				if oper == ">": 
					result = lOp > rOp
				if oper == "<": 
					result = lOp < rOp
				if oper == "<>": 
					result = lOp != rOp
				if oper == "==": 
					result = lOp == rOp
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
				types.push(resType)
				temp += 1
			else:
				print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
				exit(0)

def p_opMatrix(t):
	'''opMatrix : EXCLAMATION addOperator
				| QUESTION addOperator
				| DOLLARSIGN addOperator '''

def p_exp(t):
	'''exp : term termA1 expFunction
		   | term termA1 '''

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
				result = 0
				if oper == "+": 
					result = lOp + rOp
				if oper == "-": 
					result = lOp - rOp
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
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
				if oper == "*": 
					result = lOp * rOp
				if oper == "/": 
					result = lOp / rOp
				temp_quad = Quadruple(oper, lOp, rOp, result)
				Quadruples.push_quad(temp_quad)
				operands.push(result)
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
			  | ID addOperand addTypeId'''

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
	temp_quad = Quadruple("print", None, None, operands.pop())
	Quadruples.push_quad(temp_quad)
	types.pop()


def p_print_param(t):
	'''print_param : Expression2 addPrint
				   | CST_STRING addPrintString '''

def p_addPrintString(t):
	'addPrintString : '
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
	'''moduleFunction : Expression2 COMA moduleFunction
					  | Expression2 RIGHTPAR
					  | '''

f = open('prog.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)