import lexer as lexer
import ply.yacc as yacc
from EstructuraDatos import *
from cuadruplos import *
from errores import Error
from maquinavirtual import executeQuads

tokens = lexer.tokens


def p_program(t):
	'program : PROGRAM ID globalTable SEMICOLON declaration programFunc main'
	print("Compilacion exitosa")
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

	#operands.print()
	#types.print()
	#operators.print()
	#Quadruples.print_all()
	#variableTable.clear()

#GlobalTable: Inicializar programa y crear variableTable
def p_globalTable(t):
	'globalTable : '
	variableTable["constants"] = {}
	# Inicializar variableTable para global scope y definir nombre y tipo del programa
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Inicializar functionDir para global scope
	functionDir[currentScope] = {}
	# Definir tipo y variables como referencia a variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]
    
def p_error(t):
	Error.syntax(t.value, t.lexer.lineno)

def p_main(t):
	'main : mainTable MAIN LEFTPAR RIGHTPAR LEFTBRACE declaration statement RIGHTBRACE'

#mainTable: Agregar main a varTable e inicializar propiedades de la funcion main. Actualizar cuadruplo main para saltar al inicio del programa
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

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

#Assignment: Genera cuadruplo en el varTable correspondiente
def p_assignment(t):
	'assignment : ID EQUAL Expression2 SEMICOLON'
	#Si id esta en currentScope, generar cuadruplo y asignar su valor en varTable
	if t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			address = variableTable[currentScope][t[1]]["address"]
			temp_quad = Quadruple("=", operands.peek(), '_', address)
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = operands.pop()
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	#Si id esta en globalScope, generar cuadruplo y asignar su valor en varTable
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			address = variableTable["global"][t[1]]["address"]
			temp_quad = Quadruple("=", operands.peek(), '_', address)
			Quadruples.push_quad(temp_quad)
			variableTable["global"][t[1]]["value"] = operands.pop()
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	else:
		Error.undefined_variable(t[1], t.lexer.lineno - 1)

#Declaration: Asignar cuadruplo start para una funcion.
def p_declaration(t):
	'''declaration : VAR declarationPDT
				   | '''
	#Asignar cuadruplo start para funcion
	functionDir[currentScope]["start"] = Quadruples.next_id

#PDT=Primitive Data Type
def p_declarationPDT(t):
	'''declarationPDT : PDT vars SEMICOLON declarationPDT
					   | '''

#PDT: Cambiar el currentType de declaracion
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

#Jump Quad if: Checar tipo y valor de la expresion y generar cuadruplo para "saltar"
def p_createJQif(t):
	'createJQif : '
	result_type = types.pop()
	#Checar tipo y valor de la expresion evaluada y generar cuadruplo
	if result_type == "int":
		# if operands.peek() == 1 or operands.peek() == 0:
		res = operands.pop()
		operator = "GOTOF"
		temp_quad = Quadruple(operator, res, '_', '_')
		Quadruples.push_quad(temp_quad)
		Quadruples.push_jump(-1)
		# else: 
		# 	Error.condition_type_mismatch(t.lexer.lineno)
	else: 
		Error.condition_type_mismatch(t.lexer.lineno)

#Update Jump Quad: Actualiza el cuadruplo con el id del cuadruplo al que debe "saltar"
def p_updateJQ(t):
	'updateJQ : '
	#Actualizar cuadruplos GOTOF
	tmp_end = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_ifElse(t):
	'''ifElse : ELSE createJQelse LEFTBRACE statement RIGHTBRACE
			  | '''

#Jump Quad else: Crear cuadruplo de "salto" para else
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

#pushJumpFor: Push al id del cuadruplo para "saltar" al stack de saltos.
def p_pushJumpFor(t):
	'pushJumpFor : '
	Quadruples.push_jump(0)

#createQuadFor: Agregar GOTOF a cuadruplos
def p_createQuadFor(t):
	'createQuadFor : '
	result_type = types.pop()
	#Checar tipo y valor de la expresion y agregar cuadruplo al stack
	if result_type == "int":
		# if operands.peek() == 1 or operands.peek() == 0:
		res = operands.pop()
		operator = "GOTOF"
		temp_quad = Quadruple(operator, res, '_', '_')
		Quadruples.push_quad(temp_quad)
		Quadruples.push_jump(-1)
		# else: 
		# 	Error.condition_type_mismatch(t.lexer.lineno)
	else: 
		Error.condition_type_mismatch(t.lexer.lineno)

#updateQuadFor: Actualizar cuadruplo GOTOF con el id del cuadruplo al cual debe "saltar"
def p_updateQuadFor(t):
	'updateQuadFor : '
	#Actualizar cuadruplo GOTOF cuando termine el for
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	tmp_quad = Quadruple("GOTO", "_", "_", tmp_rtn)
	Quadruples.push_quad(tmp_quad)
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

#forAssignment: Agrega iterador a la tabla de constantes y crea una variable iterativa
def p_forAssignment(t):
	'forAssignment : ID EQUAL CST_INT'
	address_type = "cInt"
	cstAddress = 0
	if t[3] not in variableTable["constants"]:
		variableTable["constants"][t[3]] = {"value": t[3], "address": addresses[address_type]}
		cstAddress = addresses[address_type]
		addresses[address_type] += 1
	else:
		cstAddress = variableTable["constants"][t[3]]["address"]
	#Checar si el id existe en currentScope y asignar su valor
	if t[1] in variableTable[currentScope]:
		address = variableTable[currentScope][t[1]]["address"]
		temp_quad = Quadruple("=", cstAddress, '_', address)
		Quadruples.push_quad(temp_quad)
		variableTable[currentScope][t[1]]["value"] = t[3]
	#Checar si el id existe en global scope y asignar su valor
	elif t[1] in variableTable["global"]:
		address = variableTable["global"][t[1]]["address"]
		temp_quad = Quadruple("=", t[3], '_', address)
		Quadruples.push_quad(temp_quad)
		variableTable["global"][t[1]]["value"] = t[3]
	else:
		Error.undefined_variable(t[1], t.lexer.lineno)


#pushLoop: Push al id del cuadruplo al stack de "saltos"
def p_pushLoop(t):
	'pushLoop : '
	Quadruples.push_jump(1)

#startLoop: Checar tipo del resultado de la expresion, generar cuadruplo y hacer push al id de salto al stack de salto.
def p_startLoop(t):
	'startLoop : '
	result_type = types.pop()
	#Checar tipo y valor de expresion y agregar cuadruplo al stack
	if result_type == "int":
		# if operands.peek() == 1 or operands.peek() == 0:
		res = operands.pop()
		operator = "GOTOF"
		# Generate Quadruple and push it to the list
		tmp_quad = Quadruple(operator, res, "_", "_")
		Quadruples.push_quad(tmp_quad)
		# Push into jump stack
		Quadruples.push_jump(-1)
		# else:
		# 	Error.condition_type_mismatch(t.lexer.lineno)
	else :
		Error.condition_type_mismatch(t.lexer.lineno)

#endLoop: Generar cuadruplo despues de que el estatuto de while termine y actualizar el GOTOF con id al final del cuadruplo loop.
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

#addVarsToTable: Agrega ID actual (y su tipo) a varTable 
def p_addVarsToTable(t):
	'addVarsToTable : '
	#Si el ID ya existe en el scope o global, dar error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Agregar ID actual a variableTable(scope)
		variableTable[currentScope][t[-1]] = {"type": currentType}
		address_type = "g"
		if currentScope != "global":
			address_type = "l"
		if currentType == "int":
			address_type += "Int"
		elif currentType == "float":
			address_type += "Float"
		else:
			address_type += "Char"
		variableTable[currentScope][t[-1]]["address"] = addresses[address_type]
		addresses[address_type] += 1
		global arrMatId
		arrMatId = t[-1]

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''

def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK setCols
				  | '''

#varsArray: Declaracion de arreglo
def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT RIGHTBRACK setRows varsMatrix
				 | '''

def p_setRows(t):
	'setRows : '
	global arrMatId
	variableTable[currentScope][arrMatId]["rows"] = t[-2]

def p_setCols(t):
	'setCols : '
	global arrMatId
	variableTable[currentScope][arrMatId]["cols"] = t[-2]

#function: Crea cuadruplo ENDFUNC y define tabla de variables locales.
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
	functionDir[currentScope]["varLength"] = Quadruples.function_quads
	Quadruples.function_quads = 0
	currentScope = "global"

def p_param(t):
	'''param : PDT ID addFuncParams functionParam
			 | '''

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

#addFuncParams: Agrega una lista de tipos de parametros al scope de la funcion.
def p_addFuncParams(t):
	'addFuncParams : '
	# Si parametro de la funcion existe en el scope, dar error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Agregar parametro de la funcion a variableTable de currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
		if "params" not in functionDir[currentScope]:
			functionDir[currentScope]["params"] = Queue()
		# Insertar currentTypes en params Queue
		functionDir[currentScope]["params"].enqueue(currentType)

#setParamLength: Asignar el numero de parametros en la funcion
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

#addTypeInt: Guardar int en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeInt(t):
	'addTypeInt : '
	types.push("int")
	address_type = "cInt"
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses[address_type], "type": "int"}
		operands.push(variableTable["constants"][t[-1]]["address"])
		addresses[address_type] += 1
	else:
		operands.push(variableTable["constants"][t[-1]]["address"])

#addTypeFloat: Guardar float en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeFloat(t):
	'addTypeFloat : '
	types.push("float")
	address_type = "cFloat"
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses[address_type], "type": "float"}
		operands.push(variableTable["constants"][t[-1]]["address"])
		addresses[address_type] += 1
	else:
		operands.push(variableTable["constants"][t[-1]]["address"])

#addTypeChar: Guardar char en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeChar(t):
	'addTypeChar : '
	types.push("char")
	address_type = "cChar"
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses[address_type]}
		operands.push(variableTable["constants"][t[-1]]["address"])
		addresses[address_type] += 1
	else:
		operands.push(variableTable["constants"][t[-1]]["address"])

#addFuncToDir: Verifica tipo de funcion e inserta la funcion al directorio de funciones con tipo, varTable y parametros.
def p_addFuncToDir(t):
	'addFuncToDir : '
	# Si la funcion existe en global scope, dar error
	if t[-1] in variableTable["global"]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		global currentScope
		global currentType
		# Agregar funcion a variableTable de currentScope
		variableTable["global"][t[-1]] = {"type": currentType}
		# Cambiar scope al nuevo id de la funcion
		currentScope = t[-1]
		# Inicializar variableTable y functionDir por nuevo id de la funcion
		variableTable[currentScope] = {}
		functionDir[currentScope] = {}
		# Definir nuevo tipo de funcion y vars como referencia a variableTable[currentScope]
		functionDir[currentScope]["type"] = currentType
		functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_Expression2(t):
    '''Expression2 : Expression3 evaluateExp2 Expression22 Expression2Nested
                       | Expression3 opMatrix 
                       | Expression3 evaluateExp2'''

def p_Expression2Nested(t):
    '''Expression2Nested : Expression3 evaluateExp2 Expression22 Expression2Nested
                             | Expression3 evaluateExp2'''

#evaluateExp2: Evalua operador y operandos de expresiones booleanas del tipo AND Y or
def p_evaluateExp2(t):
	'evaluateExp2 : '
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
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(lOp, rOp,t.lexer.lineno)

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

#evaluateExp3: Evalua operador y operandos de expresiones booleanas del tipo >, < , == , y <>.
def p_evaluateExp3(t):
	'evaluateExp3 : '
	if operators.size() != 0:
		# Generar cuadruplos para operadores de comparacion
		if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek() == "==":
			# Pop a operandos
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop a operador
			oper = operators.pop()
			# Pop a tipos
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico para tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo del resultado y evaluar expresion
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(lOp, rOp, t.lexer.lineno)


def p_opMatrix(t):
	'''opMatrix : EXCLAMATION addOperator
				| QUESTION addOperator
				| DOLLARSIGN addOperator '''

def p_exp(t):
	'''exp : term evaluateTerm expFunction
		   | term evaluateTerm '''

#evaluateTerm: evalua operador y operandos del tipo + y - para variables y variables dimensionadas.
def p_evaluateTerm(t):
	'evaluateTerm : '
	if operators.size() != 0:
		# Generar cuadruplos para operadores de suma y resta
		if operators.peek() == "+" or operators.peek() == "-":
			# Pop a operandos
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop al operador
			oper = operators.pop()
			# Pop a tipos
			rType = types.pop()
			lType = types.pop()
			#Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(lOp, rOp, t.lexer.lineno)


def p_expFunction(t):
    '''expFunction : PLUS addOperator exp
                   | MINUS addOperator exp '''

#setVoidType: Define tipo de funcion como Void
def p_setVoidType(t):
	'setVoidType : '
	# Definir void como currentType
	global currentType
	currentType = t[-1]

def p_term(t):
        '''term : factor evaluateFactor termFunction
            | factor evaluateFactor'''

#evaluateFactor: Evalua operador y operandos el tipo * y / para variables y variables dimensionadas (multiplicacion)
def p_evaluateFactor(t):
	'evaluateFactor : '
	if operators.size() != 0:
		# Generar cuadruplos para operadores de division y multiplicacion
		if operators.peek() == "*" or operators.peek() == "/":
			# Pop a operandos
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop a operadores
			oper = operators.pop()
			# Pop a tipos
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion
			if resType != "error":
				address_type = "t"
				if resType == "int":
					address_type += "Int"
				elif resType == "float":
					address_type += "Float"
				else:
					address_type += "Char"
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				Quadruples.push_quad(temp_quad)
				operands.push(addresses[address_type])
				addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(lOp, rOp,t.lexer.lineno)
				
def p_termFunction(t):
	'''termFunction : MULTIPLY addOperator term
					| DIVIDE addOperator term '''

#addOperator: Push a operador read al stack de operadores
def p_addOperator(t):
	'addOperator : '
	operators.push(t[-1])

def p_factor(t):
	'''factor : LEFTPAR addParenthesis Expression2 RIGHTPAR removeParenthesis
			  | cst_PDT
			  | module
			  | ID addOperandId addTypeId'''

def p_addParenthesis(t):
	'addParenthesis : '
	operators.push("(")

def p_removeParenthesis(t):
	'removeParenthesis : '
	operators.pop()


#def p_addOperand(t):
	#'addOperand : '
	#operands.push(t[-1])

#addTypeId: ***
def p_addTypeId(t):
	'addTypeId : '
	#Hacer push a los tipos al stack de tipos
	if t[-2] in variableTable[currentScope]:
		types.push(variableTable[currentScope][t[-2]]["type"])
	elif t[-2] in variableTable["global"]:
		types.push(variableTable["global"][t[-2]]["type"])
	else:
		Error.undefined_variable(t[-1], t.lexer.lineno)

#addOperandId: ***
def p_addOperandId(t):
	'addOperandId : '
	#Agregar el valor del operando de currentcope al stack de operandos
	if t[-1] in variableTable[currentScope]:
		if "value" in variableTable[currentScope][t[-1]]:
			operands.push(variableTable[currentScope][t[-1]]["address"])
		else:
			Error.variable_has_no_assigned_value(t[-1], t.lexer.lineno)
	#Agregar el valor del operando de global scope al stack de operandos
	elif t[-1] in variableTable["global"]:
		if "value" in variableTable["global"][t[-1]]:
			operands.push(variableTable["global"][t[-1]]["address"])
		else:
			Error.variable_has_no_assigned_value(t[-1], t.lexer.lineno)
	else:
		Error.undefined_variable(t[-1], t.lexer.lineno)


def p_read(t):
	'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
	'id_list : ID addRead id_listFunction'

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

#addRead: Genera un cuadruplo read y le hace push a la lista de cuadruplos
def p_addRead(t):
	'addRead : '
	#Genera cuadruplo Read
	if t[-1] in variableTable[currentScope]:
		variableTable[currentScope][t[-1]]["value"] = "readValue"
		address = variableTable[currentScope][t[-1]]["address"]
		temp_quad = Quadruple("read", '_', '_', address)
		Quadruples.push_quad(temp_quad)
	elif t[-1] in variableTable["global"]:
		variableTable["global"][t[-1]]["value"] = "readValue"
		address = variableTable["global"][t[-1]]["address"]
		temp_quad = Quadruple("read", '_', '_', address)
		Quadruples.push_quad(temp_quad)
	else:
		Error.undefined_variable(t[-1], t.lexer.lineno)

def p_print(t):
	'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_printFunction2(t):
	'printFunction2 : printFunction'

#addPrint: Genera un cuadruplo print y le hace push a la lista de cuadruplos
def p_addPrint(t):
	'addPrint : '
	#Genera cuadruplo print
	temp_quad = Quadruple("print", '_', '_', operands.pop())
	Quadruples.push_quad(temp_quad)
	types.pop()


def p_print_param(t):
	'''print_param : Expression2 addPrint
				   | CST_STRING addPrintString '''

#addPrintString: Lee un string y lo guarda en la tabla de constantes para luego imprimpirlo con el operador PRINT
def p_addPrintString(t):
	'addPrintString : '
	#Agrega string al cuadruplo print
	address = 0
	if t[-1] not in variableTable["constants"]:
		variableTable["constants"][t[-1]] = {"address": addresses["cChar"]}
		address = variableTable["constants"][t[-1]]["address"]
		addresses["cChar"] += 1
	else:
		address = variableTable["constants"][t[-1]]["address"]
	temp_quad = Quadruple("print", '_', '_', address)
	Quadruples.push_quad(temp_quad)

def p_module(t):
	'module : ID checkFunctionExists generateERASize LEFTPAR moduleFunction nullParam RIGHTPAR generateGosub SEMICOLON'

#checkFunctionExists: Verifica que la funcion existe en el directorio de Funciones y le hace push al operador del modulo al stack.
def p_checkFunctionExists(t):
	'checkFunctionExists : '
	if t[-1] not in functionDir:
		Error.undefined_module(t[-1], t.lexer.lineno)
	global funcName
	funcName = t[-1]

#generateERASize: Crea el cuadruplo ERA con el directorio de la funcion que sera llamada.
def p_generateERASize(t):
	'generateERASize : '
	#Generar tamano ERA pendiente...
	global funcName
	tmp_quad = Quadruple("ERA", funcName, "_", "_")
	Quadruples.push_quad(tmp_quad)
	global k
	k = 1

#nullParam: Lanza error si falta un parametro en una llamada de funcion
def p_nullParam(t):
	'nullParam : '
	global k
	global funcName
	if k < len(functionDir[funcName]["params"].values()):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)

#generateGosub: Crea el cuadruplo Gosub con la direccion de la funcion a llamar **
def p_generateGosub(t):
	'generateGosub : '
	tmp_quad = Quadruple("GOSUB", funcName, "_", functionDir[funcName]["start"])
	Quadruples.push_quad(tmp_quad)
#generateParam: Crea el cuadruplo PARAM con el opreando que esta siendo leido.
def p_generateParam(t):
	'generateParam : '
	global k
	arg = operands.pop()
	argType = types.pop()
	paramList = functionDir[funcName]["params"].values()
	if k > len(paramList):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)
	if argType == paramList[-k]:
		tmp_quad = Quadruple("PARAM", arg, '_', "param%d" % k)
		Quadruples.push_quad(tmp_quad)
	else:
		Error.type_mismatch_module(funcName, t.lexer.lineno)

#nextParam: agrega 1 al iterador de param.
def p_nextParam(t):
	'nextParam : '
	global k
	k += 1

def p_dimensionedID(t):
	'dimensionedID : ID dimArray'

def p_dim1(t):
	'''dimArray : LEFTBRACK CST_INT RIGHTBRACK dimMatrix
				| '''

def p_dim2(t):
	'''dimMatrix : LEFTBRACK CST_INT RIGHTBRACK
				 | '''

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
	'''moduleFunction : Expression2 generateParam nextParam COMA moduleFunction
					  | Expression2 generateParam
					  | '''

f = open('test.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)

executeQuads()