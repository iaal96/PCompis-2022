import lexer as lexer
import ply.yacc as yacc
from EstructuraDatos import *
from cuadruplos import *
from errores import Error
from maquinavirtual import executeQuads

tokens = lexer.tokens
arrMatId = Stack()
arrMatScope = Stack()

def p_program(t):
	'program : PROGRAM ID globalTable SEMICOLON declaration programFunc main'
	#print("Compilacion exitosa")
	# Mostrar variable table y directorio de funciones
	'''print()
	print(variableTable["constants"])
	for i in functionDir:
	 	print("\tfunction name: %s" % i)
	 	print("\t\ttype: %s" % functionDir[i]["type"])
	 	print("\t\tvars: %s" % functionDir[i]["vars"])
	 	if "params" in functionDir[i]:
	 		print("\t\tparams: %s" % functionDir[i]["params"].values())
	 		print("\t\tparamsLength: %d" % functionDir[i]["paramsLength"])
	 		print("\t\tstart: %d" % functionDir[i]["start"])
	 		print("\t\tvarLength: %d" % functionDir[i]["varLength"])
	 	print()'''
	

	#operands.print()
	#types.print()
	#operators.print()
	Quadruples.print_all()
	#variableTable.clear()
	#arrMatOperands.print()

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
	tmp_quad = Quadruple("GOTO", "_", "_", "_")
	Quadruples.push_quad(tmp_quad)
	Quadruples.push_jump(-1)
    
def p_error(t):
	'error : '

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
	Quadruples.update_jump_quad(Quadruples.pop_jump(), Quadruples.next_id)

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

#Assignment: Genera cuadruplo en el varTable correspondiente
def p_assignment(t):
	'assignment : ID dimArray EQUAL Expression2 SEMICOLON'
	#Si id esta en currentScope, generar cuadruplo y asignar su valor en varTable
	if arrMatOperands.size() > 1:
		types.pop()
		operands.pop()
		operands.pop()
		assign = arrMatOperands.pop()
		address = arrMatOperands.pop()
		if assign["type"] != address["type"]:
			Error.type_mismatch_array_assignment(t.lexer.lineno)
		if assign["rows"] != address["rows"] or assign["cols"] != address["cols"]:
			Error.dimensions_do_not_match(t.lexer.lineno-1)
		temp_quad = Quadruple("ARR=", assign, "_", address)
		Quadruples.push_quad(temp_quad)
	elif arrMatOperands.size() == 1:
		Error.invalid_assignment_to_array_variable(t.lexer.lineno-1)
		# Error class call
	elif t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			if "rows" in variableTable[currentScope][t[1]]:
				types.pop()
				assign = operands.pop()
				address = operands.pop()
				temp_quad = Quadruple("=", assign, "_", address)
			else:
				types.pop()
				address = variableTable[currentScope][t[1]]["address"]
				temp_quad = Quadruple("=", operands.pop(), '_', address)
				operands.pop()
			Quadruples.push_quad(temp_quad)
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	#Si id esta en globalScope, generar cuadruplo y asignar su valor en varTable
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			if "rows" in variableTable["global"][t[1]]:
				types.pop()
				assign = operands.pop()
				address = operands.pop()
				temp_quad = Quadruple("=", assign, "_", address)
			else:
				types.pop()
				address = variableTable["global"][t[1]]["address"]
				temp_quad = Quadruple("=", operands.pop(), '_', address)
				operands.pop()
			Quadruples.push_quad(temp_quad)
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
		res = operands.pop()
		operator = "GOTOF"
		temp_quad = Quadruple(operator, res, '_', '_')
		Quadruples.push_quad(temp_quad)
		Quadruples.push_jump(-1)
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
		res = operands.pop()
		operator = "GOTOF"
		temp_quad = Quadruple(operator, res, '_', '_')
		Quadruples.push_quad(temp_quad)
		Quadruples.push_jump(-1)
	else: 
		Error.condition_type_mismatch(t.lexer.lineno)

#updateQuadFor: Actualizar cuadruplo GOTOF con el id del cuadruplo al cual debe "saltar"
def p_updateQuadFor(t):
	'updateQuadFor : '
	#Actualizar cuadruplo GOTOF cuando termine el for
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	tmp_quad = Quadruple("GOTOFOR", "_", "_", tmp_rtn)
	Quadruples.push_quad(tmp_quad)
	tmp_count = Quadruples.next_id
	Quadruples.update_jump_quad(tmp_end, tmp_count)

#forAssignment: Agrega iterador a la tabla de constantes y crea una variable iterativa
def p_forAssignment(t):
	'forAssignment : ID EQUAL CST_INT addTypeInt'
	address_type = "cInt"
	cstAddress = 0
	if t[3] not in variableTable["constants"]:
		variableTable["constants"][t[3]] = {"address": addresses[address_type], "type": "int"}
		cstAddress = addresses[address_type]
		addresses[address_type] += 1
	else:
		cstAddress = variableTable["constants"][t[3]]["address"]
	#Checar si el id existe en currentScope y asignar su valor
	if "rows" not in variableTable[currentScope][t[1]]:
		#Checar si el id existe en currentScope y asignar su valor
		if t[1] in variableTable[currentScope]:
			address = variableTable[currentScope][t[1]]["address"]
			temp_quad = Quadruple("=", cstAddress, '_', address)
			Quadruples.push_quad(temp_quad)
		#Checar si el id existe en global scope y asignar su valor
		elif t[1] in variableTable["global"]:
			address = variableTable["global"][t[1]]["address"]
			temp_quad = Quadruple("=", t[3], '_', address)
			Quadruples.push_quad(temp_quad)
		else:
			Error.undefined_variable(t[1], t.lexer.lineno)
	else:
		Error.invalid_assignment_to_array_variable(t.lexer.lineno)
		# Actualizar con clase error


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
		res = operands.pop()
		operator = "GOTOF"
		# Generate Quadruple and push it to the list
		tmp_quad = Quadruple(operator, res, "_", "_")
		Quadruples.push_quad(tmp_quad)
		# Push into jump stack
		Quadruples.push_jump(-1)
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
		arrMatId = Stack()
		arrMatId.push(t[-1])

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''


def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setCols
				  | '''

#varsArray: Declaracion de arreglo
def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setRows varsMatrix
				 | '''
	address_type = "g"
	const_address = "c"
	if currentScope != "global":
		address_type = "l"
	if currentType == "int":
		address_type += "Int"
		const_address += "Int"
	if currentType == "float":
		address_type += "Float"
		const_address += "Float"
	if currentType == "char":
		address_type += "Char"
		const_address += "Char"
	global arrMatId
	arrMatAddress = variableTable[currentScope][arrMatId.peek()]["address"]
	if "rows" in variableTable[currentScope][arrMatId.peek()] and "cols" not in variableTable[currentScope][arrMatId.peek()]:
		rows = variableTable[currentScope][arrMatId.peek()]["rows"]
		addresses[address_type] += rows - 1
		variableTable["constants"][arrMatAddress] = {"address": addresses[const_address], "type": "int"}
		addresses[const_address] += 1
	if "cols" in variableTable[currentScope][arrMatId.peek()]:
		rows = variableTable[currentScope][arrMatId.peek()]["rows"]
		cols = variableTable[currentScope][arrMatId.peek()]["cols"]
		addresses[address_type] += rows * cols - 1
		variableTable["constants"][arrMatAddress] = {"address": addresses[const_address], "type": "int"}
		addresses[const_address] += 1
	arrMatId.pop()

def p_setRows(t):
	'setRows : '
	global arrMatId
	if int(t[-3]) > 0:
		variableTable[currentScope][arrMatId.peek()]["rows"] = int(t[-3])
		operands.pop()
		types.pop()
	else:
		Error.array_size_must_be_positive(arrMatId.peek(), t.lexer.lineno)


def p_setCols(t):
	'setCols : '
	global arrMatId
	if int(t[-3]) > 0:
		variableTable[currentScope][arrMatId.peek()]["cols"] = int(t[-3])
		operands.pop()
		types.pop()
	else:
		Error.array_size_must_be_positive(arrMatId.peek(), t.lexer.lineno)


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
	functionDir[currentScope]["varLength"] = len(functionDir[currentScope]["vars"])
	Quadruples.function_quads = 0
	currentScope = "global"
	# Resetear direcciones locales
	addresses["lInt"] -= addresses["lInt"] % 1000
	addresses["lFloat"] -= addresses["lFloat"] % 1000
	addresses["lChar"] -= addresses["lChar"] % 1000
	global returnMade
	returnMade = False

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
		if currentType == "int":
			variableTable[currentScope][t[-1]]["address"] = addresses["lInt"]
			addresses["lInt"] += 1
		elif currentType == "float":
			variableTable[currentScope][t[-1]]["address"] = addresses["lFloat"]
			addresses["lFloat"] += 1
		else:
			variableTable[currentScope][t[-1]]["address"] = addresses["lChar"]
			addresses["lChar"] += 1
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
		if currentType == "int":
			address = addresses["gInt"]
			addresses["gInt"] += 1
		elif currentType == "float":
			address = addresses["gFloat"]
			addresses["gFloat"] += 1
		elif currentType == "char":
			address = addresses["gChar"]
			addresses["gChar"] += 1
		else:
			address = addresses["void"]
		variableTable["global"][t[-1]]["address"] = address
		# Cambiar scope al nuevo id de la funcion
		currentScope = t[-1]
		# Inicializar variableTable y functionDir por nuevo id de la funcion
		variableTable[currentScope] = {}
		functionDir[currentScope] = {}
		# Definir nuevo tipo de funcion y vars como referencia a variableTable[currentScope]
		functionDir[currentScope]["type"] = currentType
		functionDir[currentScope]["vars"] = variableTable[currentScope]
		functionDir[currentScope]["params"] = Queue()

def p_Expression2(t):
    '''Expression2 : supExpression evaluateExp2 OperatorExpression2
                       | supExpression opMatrix evaluateOpMatrix
                       | supExpression evaluateExp2'''

def p_evaluateOpMatrix(t):
	'evaluateOpMatrix : '
	if operators.size() != 0:
		if operators.peek() == "!" or operators.peek() == "?" or operators.peek() == "$":
			# Pop operands
			operands.pop()
			# Pop operator
			oper = operators.pop()
			# Pop types
			operandType = types.pop()
			# Check semanticCube with types and operator
			resType = semanticCube[(operandType, operandType, oper)]
			oper = "ARR" + oper
			if oper == "ARR!" or oper == "ARR?":
				if arrMatOperands.size() > 1:
					arrOperand = arrMatOperands.pop()
					if "cols" not in arrOperand:
						arrOperand["cols"] = 1
					if (arrOperand["rows"] == arrOperand["cols"] and oper == "ARR?") or oper == "ARR!":
						if resType != "error":
							address_type = "t"
							if resType == "int":
								address_type += "Int"
							elif resType == "float":
								address_type += "Float"
							else:
								address_type += "Char"
							temp_quad = Quadruple(oper, arrOperand, "_", addresses[address_type])
							Quadruples.push_quad(temp_quad)
							operands.push(addresses[address_type])
							if oper == "ARR?":
								arrMatOperands.push({
									"address": addresses[address_type],
									"rows": arrOperand["rows"],
									"cols": arrOperand["cols"],
									"type": "float"
								})
								addresses[address_type] += arrOperand["rows"] * arrOperand["cols"]
							elif oper == "ARR!":
								arrMatOperands.push({
									"address": addresses[address_type],
									"rows": arrOperand["cols"],
									"cols": arrOperand["rows"],
									"type": resType
								})
								addresses[address_type] += arrOperand["rows"] * arrOperand["cols"]
							types.push(resType)
						else:
							Error.invalid_operation_in_line(t.lexer.lineno)
					else:
						Error.invalid_inverse_calculation(t.lexer.lineno)
				else:
					Error.invalid_operation_in_line(t.lexer.lineno)
			else:
				arrOperand = arrMatOperands.pop()
				if arrOperand["rows"] == arrOperand["cols"]:
					if resType != "error":
						address_type = "t"
						if resType == "int":
							address_type += "Int"
						elif resType == "float":
							address_type += "Float"
						else:
							address_type += "Char"
						temp_quad = Quadruple(oper, arrOperand, "_", addresses[address_type])
						Quadruples.push_quad(temp_quad)
						operands.push(addresses[address_type])
						addresses[address_type] += 1
						types.push(resType)
					else:
						Error.invalid_operation_in_line(t.lexer.lineno)
				else:
					Error.invalid_determinant_calculation(t.lexer.lineno)

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
			if arrMatOperands.size() > 0:
				Error.invalid_operation_in_line(t.lexer.lineno)
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
				Error.operation_type_mismatch(t.lexer.lineno)

def p_OperatorExpression2(t):
    '''OperatorExpression2 : AND addOperator
                    | OR addOperator'''

def p_supExpression(t):
    '''supExpression : exp evaluatesupExp OperatorsupExpression exp evaluatesupExp
                       | exp evaluatesupExp'''

def p_OperatorsupExpression(t):
	'''OperatorsupExpression : GT addOperator
						 | LT addOperator
						 | NOTEQUAL addOperator 
						 | ISEQUAL addOperator'''

#evaluatesupExp: Evalua operador y operandos de expresiones booleanas del tipo >, < , == , y <>.
def p_evaluatesupExp(t):
	'evaluatesupExp : '
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
			if arrMatOperands.size() > 0:
				Error.invalid_operation_in_line(t.lexer.lineno)
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
				Error.operation_type_mismatch(t.lexer.lineno)


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
			# Checar y validar operandos y tamanos del arreglo.
			if arrMatOperands.size() > 1:
				rId = arrMatOperands.pop()
				lId = arrMatOperands.pop()
				# Validate equal dimensions
				if "cols" not in lId:
					lId["cols"] = 1
				if "cols" not in rId:
					rId["cols"] = 1
				if lId["rows"] == rId["rows"] and lId["cols"] == rId["cols"]:
					if oper == "+":
						oper = "ARR+"
					else:
						oper = "ARR-"
					lOp = {
						"address": lId["address"],
						"rows": lId["rows"],
						"cols": lId["cols"]
					}
					rOp = {
						"address": rId["address"],
						"rows": rId["rows"],
						"cols": rId["cols"]
					}
				else:
					Error.dimensions_do_not_match(t.lexer.lineno)
					# Error class call
			elif arrMatOperands.size() == 1:
				Error.invalid_operation_in_line(t.lexer.lineno)
				# Error class call
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
				if oper == "ARR+" or oper == "ARR-":
					arrMatOperands.push({
						"address": addresses[address_type],
						"rows": lOp["rows"],
						"cols": lOp["cols"],
						"type": resType
					})
					addresses[address_type] += lOp["rows"] * lOp["cols"]
				else:
					addresses[address_type] += 1
				types.push(resType)
			else:
				Error.operation_type_mismatch(t.lexer.lineno)


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
			# Check and validate for array or matrix operands and sizes
			if arrMatOperands.size() > 1:
				rId = arrMatOperands.pop()
				lId = arrMatOperands.pop()
				# Validate equal dimensions
				if "cols" not in lId:
					lId["cols"] = 1
				if "cols" not in rId:
					rId["cols"] = 1
				if lId["cols"] == rId["rows"]:
					if oper == "*":
						oper = "ARR*"
					else:
						Error.invalid_operator_on_arrays(t.lexer.lineno)
						# Error class call
					lOp = {
						"address": lId["address"],
						"rows": lId["rows"],
						"cols": lId["cols"]
					}
					rOp = {
						"address": rId["address"],
						"rows": rId["rows"],
						"cols": rId["cols"]
					}
				else:
					Error.invalid_operation_in_line(t.lexer.lineno)
			elif arrMatOperands.size() == 1:
				Error.invalid_operation_in_line(t.lexer.lineno)
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
				if oper == "ARR*":
					arrMatOperands.push({
						"address": addresses[address_type],
						"rows": lOp["rows"],
						"cols": rOp["cols"],
						"type": resType
					})
					addresses[address_type] += lOp["rows"] * rOp["cols"]
				types.push(resType)
			else:
				Error.operation_type_mismatch(t.lexer.lineno)
				
def p_termFunction(t):
	'''termFunction : MULTIPLY addOperator term
					| DIVIDE addOperator term '''

#addOperator: Push a operador read al stack de operadores
def p_addOperator(t):
	'addOperator : '
	# Agregar operador recibido al stack
	operators.push(t[-1])

def p_factor(t):
	'''factor : LEFTPAR addPriorityFF Expression2 RIGHTPAR removePriorityFF
			  | cst_PDT
			  | module
			  | ID dimArray'''

def p_addPriorityFF(t):
	'addPriorityFF : '
	# Agregar "fondo falso" para prioridad
	operators.push("(")

def p_removePriorityFF(t):
	'removePriorityFF : '
	# Quitar "fondo falso"
	operators.pop()


#def p_addOperand(t):
	#'addOperand : '
	#operands.push(t[-1])

def p_read(t):
	'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
	'id_list : ID dimArray addRead id_listFunction'

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

#addRead: Genera un cuadruplo read y le hace push a la lista de cuadruplos
def p_addRead(t):
	'addRead : '
	#Genera cuadruplo Read
	if t[-2] in variableTable[currentScope]:
		address = variableTable[currentScope][t[-2]]["address"]
		temp_quad = Quadruple("read", '_', '_', address)
		Quadruples.push_quad(temp_quad)
	elif t[-2] in variableTable["global"]:
		address = variableTable["global"][t[-2]]["address"]
		temp_quad = Quadruple("read", '_', '_', address)
		Quadruples.push_quad(temp_quad)
	else:
		Error.undefined_variable(t[-2], t.lexer.lineno)

def p_print(t):
	'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_printFunction2(t):
	'printFunction2 : printFunction'

def p_print_param(t):
	'''print_param : Expression2 addPrint
				   | CST_STRING addPrintString '''

#addPrintString: Lee un string y lo guarda en la tabla de constantes para luego imprimpirlo con el operador PRINT
def p_addPrintString(t):
	'addPrintString : '
	#Agrega string al cuadruplo print
	address = 0
	stringToPrint = t[-1][1:len(t[-1]) - 1]
	if stringToPrint not in variableTable["constants"]:
		variableTable["constants"][stringToPrint] = {"address": addresses["cChar"]}
		address = variableTable["constants"][stringToPrint]["address"]
		addresses["cChar"] += 1
	else:
		address = variableTable["constants"][stringToPrint]["address"]
	temp_quad = Quadruple("print", '_', '_', address)
	Quadruples.push_quad(temp_quad)

def p_addPrint(t):
	'addPrint : '
	# Generar cuadruplo print
	if arrMatOperands.size() > 0:
		Error.invalid_print_on_array_variable(t.lexer.lineno)
	temp_quad = Quadruple("print", '_', '_', operands.pop())
	Quadruples.push_quad(temp_quad)
	types.pop()


def p_module(t):
	'module : ID checkFunctionExists generateERASize LEFTPAR moduleFunction nullParam RIGHTPAR generateGosub'

#checkFunctionExists: Verifica que la funcion existe en el directorio de Funciones y le hace push al operador del modulo al stack.
def p_checkFunctionExists(t):
	'checkFunctionExists : '
	if t[-1] not in functionDir:
		Error.undefined_module(t[-1], t.lexer.lineno)
	global funcName
	funcName = t[-1]
	operators.push("module")
	types.push(functionDir[funcName]["type"])

#generateERASize: Crea el cuadruplo ERA con el directorio de la funcion que sera llamada.
def p_generateERASize(t):
	'generateERASize : '
	#Generar tamano ERA pendiente...
	global funcName
	tmp_quad = Quadruple("ERA", variableTable["global"][funcName]["address"], "_", "_")
	Quadruples.push_quad(tmp_quad)
	global paramNum
	paramNum = 1

#nullParam: Lanza error si falta un parametro en una llamada de funcion
def p_nullParam(t):
	'nullParam : '
	global paramNum
	global funcName
	if paramNum < len(functionDir[funcName]["params"].values()):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)

#generateGosub: Crea el cuadruplo Gosub con la direccion de la funcion a llamar **
def p_generateGosub(t):
	'generateGosub : '
	global funcName
	tmp_quad = Quadruple("GOSUB", variableTable["global"][funcName]["address"], "_", functionDir[funcName]["start"])
	Quadruples.push_quad(tmp_quad)
	if functionDir[funcName]["type"] != "void":
		if functionDir[funcName]["type"] == "int":
			tmpAddress = addresses["tInt"]
			addresses["tInt"] += 1
		if functionDir[funcName]["type"] == "float":
			tmpAddress = addresses["tFloat"]
			addresses["tFloat"] += 1
		if functionDir[funcName]["type"] == "char":
			tmpAddress = addresses["tChar"]
			addresses["tChar"] += 1
		tmp_quad = Quadruple("=", variableTable["global"][funcName]["address"], "_", tmpAddress)
		Quadruples.push_quad(tmp_quad)
		operands.push(tmpAddress)
		types.push(variableTable["global"][funcName]["type"])
	operators.pop()


#generateParam: Crea el cuadruplo PARAM con el opreando que esta siendo leido.
def p_generateParam(t):
	'generateParam : '
	global funcName
	global paramNum
	if arrMatOperands.size() > 0:
		Error.array_parameter_in_module_call(t.lexer.lineno)
	arg = operands.pop()
	argType = types.pop()
	paramList = functionDir[funcName]["params"].values()
	counter = paramNum
	if paramNum > len(paramList):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)
	if argType == paramList[-paramNum]:
		for var in functionDir[funcName]["vars"]:
			if counter == 1:
				address = functionDir[funcName]["vars"][var]["address"]
			counter -= 1
		tmp_quad = Quadruple("PARAM", arg, '_', address)
		Quadruples.push_quad(tmp_quad)
	else:
		Error.type_mismatch_module(funcName, t.lexer.lineno)

#nextParam: agrega 1 al iterador de param.
def p_nextParam(t):
	'nextParam : '
	global paramNum
	paramNum += 1

def p_dimArray(t):
	'''dimArray : addOperandId addTypeId LEFTBRACK readIDType Expression2 verifyRows RIGHTBRACK dimMatrix
				| addOperandId addTypeId '''
	global arrMatId
	arrMatId.pop()
	arrMatScope.pop()

def p_addOperandId(t):
	'addOperandId : '
	# Agregar ID de variable dimensionada a stack
	arrMatId.push(t[-1])
	# Agregar valor del operando de currentScope a stack de operandos
	if arrMatId.peek() in variableTable[currentScope]:
		operands.push(variableTable[currentScope][arrMatId.peek()]["address"])
		arrMatScope.push(currentScope)
	# Agregar valor del operando de globalScope a stack de operandos
	elif arrMatId.peek() in variableTable["global"]:
		operands.push(variableTable["global"][arrMatId.peek()]["address"])
		arrMatScope.push("global")
	else:
		Error.undefined_variable(arrMatId.peek(), t.lexer.lineno)
	if "rows" in variableTable[arrMatScope.peek()][t[-1]]:
		if "cols" not in variableTable[arrMatScope.peek()][t[-1]]:
			variable = variableTable[arrMatScope.peek()][t[-1]]
			arrMatOperands.push({
				"address": variable["address"],
				"rows": variable["rows"],
				"cols": 1
			})
		else:
			arrMatOperands.push(variableTable[arrMatScope.peek()][t[-1]])

def p_addTypeId(t):
	'addTypeId : '
	# Push a tipos a la pila de tipos
	if arrMatId.peek() in variableTable[currentScope]:
		types.push(variableTable[currentScope][arrMatId.peek()]["type"])
	elif arrMatId.peek() in variableTable["global"]:
		types.push(variableTable["global"][arrMatId.peek()]["type"])
	else:
		Error.undefined_variable(arrMatId.peek(), t.lexer.lineno)

def p_readIDType(t):
	'readIDType : '
	global arrMatId
	operands.pop()
	operators.push("Mat")
	arrMatOperands.pop()
	if arrMatId.peek() in variableTable[currentScope]:
		if types.pop() != variableTable[currentScope][arrMatId.peek()]["type"]:
			Error.type_mismatch(arrMatId.peek(), t.lexer.lineno)
		if "rows" not in variableTable[currentScope][arrMatId.peek()]:
			Error.variable_not_subscriptable_as_array(arrMatId.peek(), t.lexer.lineno)
	elif arrMatId.peek() in variableTable["global"]:
		if types.pop() != variableTable["global"][arrMatId.peek()]["type"]:
			Error.type_mismatch(arrMatId.peek(), t.lexer.lineno)
		if "rows" not in variableTable["global"][arrMatId.peek()]:
			Error.variable_not_subscriptable_as_array(arrMatId.peek(), t.lexer.lineno)

def p_verifyRows(t):
	'verifyRows : '
	if types.pop() != "int":
		Error.type_mismatch_in_index(arrMatId.peek(), t.lexer.lineno)
	baseAdd = variableTable[arrMatScope.peek()][arrMatId.peek()]["address"]
	upperLim = baseAdd + variableTable[arrMatScope.peek()][arrMatId.peek()]["rows"] - 1
	tmp_quad = Quadruple("VERIFY", operands.peek(), baseAdd, upperLim)
	Quadruples.push_quad(tmp_quad)

def p_dimMatrix(t):
	'''dimMatrix : LEFTBRACK Expression2 verifyCols RIGHTBRACK
				 | checkMatAsArray '''
	operators.pop()
	address_type = "t"
	if variableTable[arrMatScope.peek()][arrMatId.peek()]["type"] == "int":
		address_type += "Int"
	elif variableTable[arrMatScope.peek()][arrMatId.peek()]["type"] == "float":
		address_type += "Float"
	else:
		address_type += "Char"
	baseAdd = variableTable[arrMatScope.peek()][arrMatId.peek()]["address"]
	addressCst = variableTable["constants"][baseAdd]["address"]
	tmp_quad = Quadruple("+", addressCst, operands.pop(), addresses["tPoint"])
	Quadruples.push_quad(tmp_quad)
	operands.push(addresses["tPoint"])
	types.push(variableTable[arrMatScope.peek()][arrMatId.peek()]["type"])
	addresses["tPoint"] += 1

def p_verifyCols(t):
	'verifyCols : '
	if "cols" not in variableTable[arrMatScope.peek()][arrMatId.peek()]:
		Error.variable_not_subscriptable_as_matrix(arrMatId, t.lexer.lineno)
	#PENDIENTE ARRAYS GLOBAL/LOCAL MIX
	if types.pop() != "int":
		Error.type_mismatch_in_index(arrMatId.peek(),t.lexer.lineno)
	# Formula de calculo de direccion al estilo C
	constant_value = str(variableTable[arrMatScope.peek()][arrMatId.peek()]["rows"])
	cstIntAddr = variableTable["constants"][constant_value]["address"]
	tmp_quad = Quadruple("*", operands.pop(), cstIntAddr, addresses["tInt"])
	Quadruples.push_quad(tmp_quad)
	operands.push(addresses["tInt"])
	addresses["tInt"] += 1
	tmp_quad = Quadruple("+", operands.pop(), operands.pop(), addresses["tInt"])
	Quadruples.push_quad(tmp_quad)
	operands.push(addresses["tInt"])
	addresses["tInt"] += 1
	#[1, [4  [7, [10,
	# 2,  5,  8,  11,
	# 3], 6], 9], 12]
	# Addre = [0,1,2,3,4,5,6,7,8,9,10,11]
	# Datos = [1,2,3,4,5,6,7,8,9,10,11,12]
	#[2][2] => 9 => address = 8 
	#[1][0] => 8 => address = 7
	# 1st + 2nd * rows
	baseAdd = variableTable[currentScope][arrMatId.peek()]["address"]
	upperLim = baseAdd + variableTable[currentScope][arrMatId.peek()]["rows"] * variableTable[currentScope][arrMatId.peek()]["cols"] - 1
	tmp_quad = Quadruple("VERIFY", operands.peek(), baseAdd, upperLim)
	Quadruples.push_quad(tmp_quad)

def p_checkMatAsArray(t):
	'checkMatAsArray : '
	global arrMatId
	if arrMatId.peek() in variableTable[currentScope]:
		if "cols" in variableTable[currentScope][arrMatId.peek()]:
			Error.matrix_accessed_as_array(arrMatId.peek(), t.lexer.lineno)
	elif arrMatId.peek() in variableTable["global"]:
		if "cols" in variableTable["global"][arrMatId.peek()]:
			Error.matrix_accessed_as_array(arrMatId.peek(), t.lexer.lineno)

def p_statement(t):
	'''statement : return checkVoidType
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | module SEMICOLON statement
				 | for statement
				 | while statement 
				 | checkNonVoidType'''

def p_checkVoidType(t):
	'checkVoidType : '
	global currentScope
	if functionDir[currentScope]["type"] == "void":
		Error.return_on_void_function(0, t.lexer.lineno)
	if types.pop() == functionDir[currentScope]["type"]:
		tmp_quad = Quadruple("RETURN", "_", "_", operands.pop())
		Quadruples.push_quad(tmp_quad)
		global returnMade
		returnMade = True
	else:
		Error.type_mismatch_on_return(t.lexer.lineno)

def p_checkNonVoidType(t):
	'checkNonVoidType : '
	if functionDir[currentScope]["type"] != "void":
		Error.no_return_on_function(0, t.lexer.lineno)

def p_moduleFunction(t):
	'''moduleFunction : Expression2 generateParam nextParam COMA moduleFunction
					  | Expression2 generateParam
					  | '''

import sys

if len(sys.argv) > 1:
	f = open(sys.argv[1], "r")
else:
	f = open("test.txt", "r")
program = f.read()

parser = yacc.yacc()

parser.parse(program)

executeQuads()