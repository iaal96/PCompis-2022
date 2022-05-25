import sys

class Error:
	@staticmethod
	def type_mismatch(t, lineno):
		" error type mismatch "
		print("Error: type mismatch en asignacion de '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def condition_type_mismatch(lineno):
		" error type mismatch en if"
		print("Error: type mismatch en expresion de condicion en la linea %d." % lineno)
		exit(0)

	@staticmethod
	def type_mismatch_module(t, lineno):
		print("Error: type mismatch en llamada de modulo '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def operation_type_mismatch(lOp, rOp, lineno):
		"error de operation type mismatch "
		print("Error: type mismatch entre '%s' y '%s' en la linea %d" % (lOp, rOp, lineno))
		exit(0)

	@staticmethod
	def undefined_variable(t,lineno):
		" error de uso de variable indefinida "
		print("Error: uso de variable indefinida '%s' en la linea %d" % (t, lineno))
		exit(0)

	@staticmethod
	def redefinition_of_variable(t, lineno):
		" error de redefinicion de variable "
		print("Error: redefinicion de variable '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_has_no_assigned_value(t, lineno):
		" error de variable sin valor asignado "
		print("Error: variable '%s' en la linea %d no tiene un valor asignado." %(t, lineno))
		exit(0)

	@staticmethod
	def syntax(t, lineno):
		" error sintactico "
		print("Error sintactico: Token '%s' inesperado en la linea %d" % (t, lineno))
		exit(0)

	@staticmethod
	def undefined_module(t, lineno):
		" error de modulo indefinido "
		print("Error: uso de modulo indefinido '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def unexpected_number_of_arguments(t, lineno):
		" error de numero equivocado de argumentos "
		print("Error: Numero inesperado de argumentos en llamada de modulo '%s' en la linea  %d." % (t, lineno))
		exit(0)