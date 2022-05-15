import lexer as lexer
import ply.yacc as yacc
from EstructuraDatos import types, operands, operators, variableTable, Queue
from EstructuraDatos import functionDir, temp, currentScope, currentType, semanticCube
from quadruples import *

tokens = lexer.tokens


def p_program(t):
	'program : PROGRAM ID globalTable SEMICOLON programVars programFunc main'
	print("Code ok")
	# Mostrar variable table y directorio de funciones
	# print()
	# for i in functionDir:
	# 	print("\tfunction name: %s" % i)
	# 	print("\t\ttype: %s" % functionDir[i]["type"])
	# 	print("\t\tvars: %s" % functionDir[i]["vars"])
	# 	if "params" in functionDir[i]:
	# 		print("\t\tparams: %s" % functionDir[i]["params"].values())
	# 		print("\t\tparamsLength: %d" % functionDir[i]["paramsLength"])
	# 		print("\t\tstart: %d" % functionDir[i]["start"])
	# 		print("\t\tvarLength: %d" % functionDir[i]["varLength"])
	# 	print()

	operands.print()
	types.print()
	operators.print()
	Quadruples.print_all()
	variableTable.clear()

#Global scope
def p_globalTable(t):
	'globalTable : '
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
	'main : mainTable MAIN LEFTPAR RIGHTPAR LEFTBRACE declaration statement RIGHTBRACE'

def p_mainTable(t):
	'mainTable : '
	global currentScope
	#Agrega main a currentScope varTable
	variableTable[currentScope]["main"] = {"type": "void"}
	currentScope = "main"
	# Inicializar variableTable y functionDir para main scope
	variableTable[currentScope] = {}
	functionDir[currentScope] = {}
	# Definir tipo de funcion y variables como referencia a variableTable["main"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_programVars(t):
	'''programVars : globalDeclaration
				   | '''

def p_globalDeclaration(t):
	'globalDeclaration : VAR declarationPDT'

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

def p_assignment(t):
	'assignment : ID EQUAL Expression2 SEMICOLON'
	#Si id esta en currentScope, generar cuadruplo y asignar su valor en varTable
	if t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			temp_quad = Quadruple("=", operands.pop(), None, t[1])
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = t[3]
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	#Si id esta en globalScope, generar cuadruplo y asignar su valor en varTable
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			temp_quad = Quadruple("=", operands.pop(), None, t[1])
			Quadruples.push_quad(temp_quad)
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_declaration(t):
	'declaration : VAR declarationPDT'
	#Asignar cuadruplo start para funcion
	functionDir[currentScope]["start"] = Quadruples.next_id

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
	#Checar tipo y valor de la expresion evaluada y generar cuadruplo
	if result_type == "int":
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			temp_quad = Quadruple(operator, res, None, None)
			Quadruples.push_quad(temp_quad)
			Quadruples.push_jump(-1)
		else: 
			print("Error: type mismatch for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else: 
		print("Error: type mismatch for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_updateJQ(t):
	'updateJQ : '
	#Actualizar cuadruplos GOTOF
	tmp_end = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	tmp_quad = Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_ifElse(t):
	'''ifElse : ELSE createJQelse LEFTBRACE statement RIGHTBRACE
			  | '''

#Jump Quad else
def p_createJQelse(t):
	'createJQelse : '
	#Crear cuadruplo para else
	operator = "GOTO"
	tmp_quad = Quadruple(operator, '_', '_', '_')
	Quadruples.push_quad(tmp_quad)
	tmp_false = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_false, tmp_count)
	Quadruples.push_jump(-1)

def p_for(t):
	'for : FOR forAssignment TO pushJumpFor Expression2 createQuadFor LEFTBRACE statement RIGHTBRACE updateQuadFor'

def p_pushJumpFor(t):
	'pushJumpFor : '
	Quadruples.push_jump(0)

def p_createQuadFor(t):
	'createQuadFor : '
	result_type = types.pop()
	#Checar tipo y valor de la expresion y agregar cuadruplo al stack
	if result_type == "int":
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			temp_quad = Quadruple(operator, res, '_', '_')
			Quadruples.push_quad(temp_quad)
			Quadruples.push_jump(-1)
		else: 
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)
	else: 
		print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)

def p_updateQuadFor(t):
	'updateQuadFor : '
	#Actualizar cuadruplo GOTOF cuando termine el for
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	tmp_quad = Quadruple("GOTO", "_", "_", tmp_rtn)
	Quadruples.push_quad(tmp_quad)
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_forAssignment(t):
	'forAssignment : ID EQUAL CST_INT'
	#Checar si el id existe en currentScope y asignar su valor
	if t[1] in variableTable[currentScope]:
		temp_quad = Quadruple("=", t[3], '_', t[1])
		Quadruples.push_quad(temp_quad)
		variableTable[currentScope][t[1]]["value"] = t[3]
	#Checar si el id existe en global scope y asignar su valor
	elif t[1] in variableTable["global"]:
		temp_quad = Quadruple("=", t[3], '_', t[1])
		Quadruples.push_quad(temp_quad)
		variableTable["global"][t[1]]["value"] = t[3]
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)


def p_pushLoop(t):
	'pushLoop : '
	Quadruples.push_jump(1)

def p_startLoop(t):
	'startLoop : '
	result_type = types.pop()
	#Checar tipo y valor de expresion y agregar cuadruplo al stack
	if result_type == "int":
		if operands.peek() == 1 or operands.peek() == 0:
			res = operands.pop()
			operator = "GOTOF"
			# Generar cuadruplo y hacerle push a la lista
			tmp_quad = Quadruple(operator, res, None, None)
			Quadruples.push_quad(tmp_quad)
			# Push al stack
			Quadruples.push_jump(-1)
		else:
			print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
			exit(0)	
	else :
		print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
		exit(0)	

def p_endLoop(t):
	'endLoop : '
	#Generar cuadruplo cuando el while termine y actualizar GOTOF
	false_jump = Quadruples.pop_jump()
	return_jump = Quadruples.pop_jump()
	tmp_quad = Quadruple("GOTO", "_", "_", return_jump-1)
	Quadruples.push_quad(tmp_quad)
	next_id = Quadruples.next_id
	Quadruples.update_jump_quad(false_jump, next_id)


def p_comment(t):
	'comment : COMMENT_TEXT'

def p_while(t):
	'while : WHILE pushLoop LEFTPAR Expression2 RIGHTPAR startLoop LEFTBRACE statement RIGHTBRACE endLoop'

def p_vars(t):
	'vars : ID addVarsToTable varsArray varsComa'

def p_addVarsToTable(t):
	'addVarsToTable : '
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
'function : functionType ID addFuncToDir LEFTPAR param RIGHTPAR setParamLength LEFTBRACE declaration statement RIGHTBRACE'
    #Resetear scope a global cuando se salga del scope de la funcion, eliminar varTable y referenciar en functionDir
    global currentScope
    #del variableTable[currentScope]
    #del functionDir[currentScope]["vars"]
	# Crear cuadruplo endfuc para terminar funcion
	temp_quad = Quadruple("ENDFUNC", "_", "_", "_")
	Quadruples.push_quad(temp_quad)
	# Variables temporales = longitud del cuadruplo de funcion al maximo y resetear func_quads
	functionDir[currentScope]["varLength"] = Quadruples.func_quads
	Quadruples.func_quads = 0
    currentScope = "global"

def p_param(t):
	'''param : PDT ID addFuncParams functionParam
			 | '''

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

def p_addFuncParams(t):
    'addFuncParams : '
    # Si parametro de la funcion ya existe en el scope ,dar error
    if t[-1] in variableTable[currentScope]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Agregar parametro funcion a variableTable de currentScope
        variableTable[currentScope][t[-1]] = {"type": currentType}
		if "params" not in functionDir[currentScope]:
			functionDir[currentScope]["params"] = Queue()
		# Agregar currentTypes en Queue params
		functionDir[currentScope]["params"].enqueue(currentType)

def p_setParamLength(t):
	'setParamLength : '
	#Asignar el numero de parametro de la funcion al tamano del Queue params
	functionDir[currentScope]["paramsLength"] = functionDir[currentScope]["params"].size()

def p_functionType(t):
	'''functionType : FUNCTION PDT
					| FUNCTION VOID setVoidType'''

def p_cst_PDT(t):
	'''cst_PDT : CST_INT addTypeInt
				| CST_FLOAT addTypeFloat
				| CST_CHAR addTypeChar'''
	t[0] = t[1]

def p_addTypeInt(t):
	'addTypeInt : '
	types.push("int")

def p_addTypeFloat(t):
	'addTypeFloat : '
	types.push("float")

def p_addTypeChar(t):
	'addTypeChar : '
	types.push("char")

def p_addFuncToDir(t):
    'addFuncToDir : '
    # Si la funcion ya existe en scope global, lanzar error
    if t[-1] in variableTable["global"]:
        print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        global currentScope
        global currentType
        # Agregar funcion a variableTable de currentScope
        variableTable["global"][t[-1]] = {"type": currentType}
        # Cambiar scope a nuevo id de la funcion
        currentScope = t[-1]
        # Inicializar variableTable y functionDir para nuevo id de la funcion
        variableTable[currentScope] = {}
        functionDir[currentScope] = {}
        # Establecer nuevo tipo de funcion y vars como referencia a variableTable[currentScope]
        functionDir[currentScope]["type"] = currentType
        functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_Expression2(t):
    '''Expression2 : Expression3 evaluateExp2 Expression22 Expression2Nested
                       | Expression3 opMatrix 
                       | Expression3 evaluateExp2'''

def p_Expression2Nested(t):
    '''Expression2Nested : Expression3 Exp2A1 Expression22 Expression2Nested
                             | Expression3 Exp2A1'''


def p_evaluateExp2(t):
	'evaluateExp2 : '
	global temp
	if operators.size() != 0:
		#Generar cuadruplos para and y or
		if operators.peek() == "|" or operators.peek() == "&":
			#Operandos pop
			rOp = operands.pop()
			lOp = operands.pop()
			#Operadores pop
			oper = operators.pop()
			#Tipos de pop
			rType = types.pop()
			lType = types.pop()
			#Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			#Checar tipo y valor
			if resType == "int":
				result = 0
				lOp = int(lOp)
				rOp = int(rOp)
				if (lOp != 0 and lOp != 1) or (rOp != 0 and rOp != 1):
					print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
					exit(0)
				#Evaluar expresion y hacerle push a cuadruplo
				if oper == "|":
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
    '''Expression3 : exp evaluateExp3 Expression33 exp evaluateExp3
                       | exp evaluateExp3'''

def p_Expression33(t):
	'''Expression33 : GT addOperator
						 | LT addOperator
						 | NOTEQUAL addOperator 
						 | ISEQUAL addOperator'''

def p_evaluateExp3(t):
	'evaluateExp3 : '
	global temp
	if operators.size() != 0:
		#Generar cuadruplos para operadores de comparacion
		if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek() == "==":
			#Operandos pop
			rOp = operands.pop()
			lOp = operands.pop()
			#Operador pop
			oper = operators.pop()
			#Tipos de pop
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico para tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion
			if resType != "error":
				result = 0
				if oper == ">": 
					result = float(lOp) > float(rOp)
				if oper == "<": 
					result = float(lOp) < float(rOp)
				if oper == "<>": 
					result = float(lOp) != float(rOp)
				if oper == "==": 
					result = float(lOp) == float(rOp)
				result = int(result)
				# Generar cuadruplo para expresion
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
	'''exp : term evaluateTerm expFunction
		   | term evaluateTerm '''

def p_evaluateTerm(t):
	'evaluateTerm : '
	global temp
	if operators.size() != 0:
		# Generar cuadruplo para operadores de suma y resta
		if operators.peek() == "+" or operators.peek() == "-":
			# Operandos pop
			rOp = operands.pop()
			lOp = operands.pop()
			# Operador pop
			oper = operators.pop()
			# Tipos de pop
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo del resultado y evaluar expresion
			if resType != "error":
				result = 0
				if oper == "+": 
					result = float(lOp) + float(rOp)
				if oper == "-": 
					result = float(lOp) - float(rOp)
				if result % 1 == 0:
					result = int(result)
				# Generar cuadruplo para expresion
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

def p_setVoidType(t):
	'setVoidType : '
	# Establecer void como currentType
	global currentType
	currentType = t[-1]

def p_term(t):
        '''term : factor evaluateFactor termFunction
            | factor evaluateFactor'''

def p_evaluateFactor(t):
	'evaluateFactor : '
	global temp
	if operators.size() != 0:
		# Generar cuadruplo para operadores de multiplicacion y division
		if operators.peek() == "*" or operators.peek() == "/":
			# Operandos pop
			rOp = operands.pop()
			lOp = operands.pop()
			# Operador pop
			oper = operators.pop()
			# Tipos de pop
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion
			if resType != "error":
				if oper == "*": 
					result = float(lOp) * float(rOp)
				if oper == "/": 
					result = float(lOp) / float(rOp)
				if result % 1 == 0:
					result = int(result)
				# Generar cuadruplo para expresion
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
			  | cst_PDT addOperandCst
			  | module
			  | ID addOperandId addTypeId'''

def p_addOperand(t):
	'addOperand : '
	operands.push(t[-1])

def p_addTypeId(t):
	'addTypeId : '
	#Hacer push a los tipos al stack de tipos
	if t[-2] in variableTable[currentScope]:
		types.push(variableTable[currentScope][t[-2]]["type"])
	elif t[-2] in variableTable["global"]:
		types.push(variableTable["global"][t[-2]]["type"])
	else:
		print("Error: use of undefined '%s' used in line %d" % (t[-1], t.lexer.lineno))


def p_addOperandCst(t):
	'addOperandCst : '
	operands.push(t[-1])


def p_addOperandId(t):
	'addOperandId : '
	#Agregar el valor del operando de currentcope al stack de operandos
	if t[-1] in variableTable[currentScope]:
		if "value" in variableTable[currentScope][t[-1]]:
			operands.push(variableTable[currentScope][t[-1]]["value"])
		else:
			print("Error: variable '%s' in line %d has not been assigned a value" %(t[-1], t.lexer.lineno))
			exit(0)
	#Agregar el valor del operando de global scope al stack de operandos
	elif t[-1] in variableTable["global"]:
		if "value" in variableTable["global"][t[-1]]:
			operands.push(variableTable["global"][t[-1]]["value"])
		else:
			print("Error: variable '%s' in line %d has not been assigned a value" %(t[-1], t.lexer.lineno))
			exit(0)
	else:
		print("Error: use of undefined variable '%s' in line %d" % (t[-1], t.lexer.lineno))
		exit(0)


def p_read(t):
	'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
	'id_list : ID addRead id_listFunction'

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

def p_addRead(t):
	'addRead : '
	#Genera cuadruplo Read
	if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
		temp_quad = Quadruple("read", None, None, t[-1])
		Quadruples.push_quad(temp_quad)
	else:
		print("Error: use of undefined variable '%s' used in line %d" % (t[-1], t.lexer.lineno))

def p_print(t):
	'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_printFunction2(t):
	'printFunction2 : printFunction'

def p_addPrint(t):
	'addPrint : '
	#Genera cuadruplo print
	temp_quad = Quadruple("print", None, None, operands.pop())
	Quadruples.push_quad(temp_quad)
	types.pop()


def p_print_param(t):
	'''print_param : Expression2 addPrint
				   | CST_STRING addPrintString '''

def p_addPrintString(t):
	'addPrintString : '
	#Agrega string al cuadruplo print
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