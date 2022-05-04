#Semantica

#Incluir estructura de datos para Stack, Queue y Tipos de Variables
from EstructuraDatos import *
import sys

#Definir clases
#Clase Var para construir las variables
#Atributos: id (unico para cada objeto), name, type (tipo de variable), value (valor asignado a la variable)
class Var:

    def __init__(self):
        self.id = -1
        self.name = ""
        self.type = 0
        self.value = None

    def erase(self):
        self.id = -1
        self.name = ""
        self.type = 0
        self.value = None

    def init_var(self, id, name, type, value):
        self.id = id
        self.name = name
        self.type = type
        self.value = value

    def print_var(self):
        	print "\t\tid: " + str(self.id) + ",\n\t\tname: " + self.name  + ",\n\t\ttype: " + str(self.type) + ",\n\t\tvalue: " + str(self.value)
		    print "\t\t---------"

#Clase Array para construir un Array
#Atributos: id (unico para cada objeto), name, type (tipo de variable), length (tamano del array)
class Array:

    def __init__(self):
        self.id = -1
        self.name = ""
        self.type = 0
        self.length = 0
    
    #Cuando no se sabe el tamano
    def init_arr(self, id, name, type, length):
        self.id = id
        self.name = name
        self.type = type
        self.length = length

    def print_arr(self):
        print "\t\tARRAY! \n\t\tid: " + str(self.id) + ",\n\t\tname: " + self.name  + ",\n\t\ttype: " + str(self.type) + ",\n\t\tlength: " + str(self.length)

    #imprimir todo
    def print_var(self):
        self.print_arr()

#Clase Function para construir funciones
#Atributos: id(unico para funciones del programa), name (nombre de funcion), type (tipo de valor de return),
#vars (diccionario de variables creadas), has_return (si la funcion utiliza return para finalizar)
class Function:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.type = 0
        self.vars = {}
        self.params = []
        self.quad_index = -1
        self.has_return = False

    def erase(self):
        self.id = -1
        self.name = ""
        self.type = 0
        self.vars = {}
        self.params = []
        self.quad_index = -1
        self.has_return = False

    def init_func(self, id, name, type, q_index):
        self.id = id
        self.name = name
        self.type = type
        self.quad_index = q_index
        self.has_return = False

#Agrega Variable al diccionario de variables de la funcion
    def add_var(self, var):
        if var.name not in self.vars:
            tmp_var = Var()
            tmp_var.init_var(None, var.name, var.type, var.value)
            #Busca el ID a asignar a la variable
            if  self.name == 'program':
                tmp_var.id = SemanticInfo.get_next_global_var_id(var.type)
            else:
                tmp_var.id = SemanticInfo.get_next_var_id(var.type)

            self.vars[var.name] = tmp_var
            return tmp_var
        else:
            Error.already_defined('variable', var.name)
            
#Agrega Array al diccionario de variables de la funcion
    def add_arr(self, arr):
        if arr.name not in self.vars:
            tmp_arr = Array()
            tmp_arr.init_arr(None, arr.name, arr.type, arr.length)

            if self.name == 'program':
                tmp_arr.id = SemanticInfo.get_next_global_var_id(arr.type)
            else:
                tmp_arr.id = SemanticInfo.get_next_var_id(arr.type)

            self.vars[arr.name] = tmp_arr
            return tmp_arr
        else:
            Error.already_defined('variable array', arr.name)