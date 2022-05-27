from cuadruplos import Quadruples
from memoria import Memory
from EstructuraDatos import variableTable
from errores import *
import re
cstMemMap = {}

globalMem = Memory()
localMem = Memory()
tempMem = Memory()

localMemStack = []
functionReturnStack = []
currentFunctionStack = []
pointerMemStack = []

def getValueFromAddress(address):
    add_type = address // 1000
    if add_type == 0:
        return globalMem.getInt(address)
    if add_type == 1:
        return globalMem.getFloat(address)
    if add_type == 2:
        return globalMem.getChar(address)
    if add_type == 3:
        return localMem.getInt(address)
    if add_type == 4:
        return localMem.getFloat(address)
    if add_type == 5:
        return localMem.getChar(address)
    if add_type == 6:
        return tempMem.getInt(address)
    if add_type == 7:
        return tempMem.getFloat(address)
    if add_type == 8:
        return tempMem.getChar(address)
    if add_type == 12:
        return pointerMemStack[address % 1000]
    else:
        return cstMemMap[address]

def executeQuads():
    for cst in variableTable["constants"]:
        if "type" in variableTable["constants"][cst]:
            if variableTable["constants"][cst]["type"] == "int":
                cstMemMap[variableTable["constants"][cst]["address"]] = int(cst)
            elif variableTable["constants"][cst]["type"] == "float":
                cstMemMap[variableTable["constants"][cst]["address"]] = float(cst)
        else:
            cstMemMap[variableTable["constants"][cst]["address"]] = cst
    index = 0
    print(cstMemMap)
    while len(Quadruples.quadruples) > index:    
        quad = Quadruples.quadruples[index]
        # quad.print()
        newIndex = executeInstruction(quad)
        if quad.operator != "+ADD":
            if newIndex:
                index = newIndex
            else:
                index += 1                    
        else:
            index += 1
            # if Quadruples.quadruples[index].operator == "UPDATEMAT":
            #     index += 1
            #     auxIndex = index
            #     while Quadruples.quadruples[index].operator != "+":
            #         index += 1
            #     Quadruples.quadruples[index].right_operand = newIndex
            #     index = auxIndex
            if Quadruples.quadruples[index].operator != "VERIFY":
                regOperators = ["+", "-", "*", "/", "="]
                if Quadruples.quadruples[index].operator != "print":
                    if Quadruples.quadruples[index].operator not in regOperators:
                        Quadruples.quadruples[index].result = newIndex
            else:
                Quadruples.quadruples[index].left_operand = newIndex

def executeInstruction(quad):
    if quad.operator == "=":
       return assign(quad)
    elif quad.operator == "+":
       return add(quad)
    elif quad.operator == "-":
       return subtract(quad)
    elif quad.operator == "*":
      return multiply(quad)
    elif quad.operator == "/":
      return divide(quad)
    elif quad.operator == ">":
       return greaterThan(quad)
    elif quad.operator == "<":
       return lessThan(quad)
    elif quad.operator == "<>":
       return notEqual(quad)
    elif quad.operator == "==":
       return equals(quad)
    elif quad.operator == "|":
       return orOp(quad)
    elif quad.operator == "&":
       return andOp(quad)
    elif quad.operator == "read":
       return read(quad)
    elif quad.operator == "print":
       return printScreen(quad)
    elif quad.operator == "ENDFUNC":
       return endFunc(quad)
    elif quad.operator == "GOTOF":
       return gotof(quad)
    elif quad.operator == "GOTO":
        return goto(quad)
    elif quad.operator == "GOTOFOR":
        return gotofor(quad)
    elif quad.operator == "GOSUB":
       return gosub(quad)
    elif quad.operator == "ERA":
       return era(quad)
    elif quad.operator == "PARAM":
        return param(quad)
    elif quad.operator == "RETURN":
        return rtn(quad)
    elif quad.operator == "VERIFY":
        return verify(quad)
    elif quad.operator == "+ADD":
        return plusAdd(quad)
    elif quad.operator == "UPDATEMAT":
        return updateMatAdd(quad)

def assign(quad):
    add_type = quad.result // 1000
    lOp = quad.left_operand // 1000
    if add_type == 0:
        if lOp == 9:
            globalMem.insertInt(cstMemMap[quad.left_operand], quad.left_operand)
        elif lOp == 6:
            globalMem.insertInt(tempMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 3:
            globalMem.insertInt(localMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 0:
            globalMem.insertInt(globalMem.getInt(quad.left_operand), quad.left_operand)
    if add_type == 1:
        if lOp == 10:
            globalMem.insertFloat(cstMemMap[quad.left_operand], quad.left_operand)
        elif lOp == 7:
            globalMem.insertFloat(tempMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 4:
            globalMem.insertFloat(localMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 1:
            globalMem.insertFloat(globalMem.getInt(quad.left_operand), quad.left_operand)
    if add_type == 2:
        if lOp == 9:
            globalMem.insertChar(cstMemMap[quad.left_operand], quad.left_operand)
        elif lOp == 6:
            globalMem.insertChar(tempMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 3:
            globalMem.insertChar(localMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 0:
            globalMem.insertChar(globalMem.getInt(quad.left_operand), quad.left_operand)
    if add_type == 3:
        if lOp == 9:
            localMem.insertInt(cstMemMap[quad.left_operand], quad.left_operand)
        elif lOp == 6:
            localMem.insertInt(tempMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 3:
            localMem.insertInt(localMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 0:
            localMem.insertInt(globalMem.getInt(quad.left_operand), quad.left_operand)
    if add_type == 4:
        if lOp == 10:
            localMem.insertFloat(cstMemMap[quad.left_operand], quad.left_operand)
        elif lOp == 7:
            localMem.insertFloat(tempMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 4:
            localMem.insertFloat(localMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 1:
            localMem.insertFloat(globalMem.getInt(quad.left_operand), quad.left_operand)
    if add_type == 5:
        if lOp == 10:
            localMem.insertChar(cstMemMap[quad.left_operand], quad.left_operand)
        elif lOp == 7:
            localMem.insertChar(tempMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 4:
            localMem.insertChar(localMem.getInt(quad.left_operand), quad.left_operand)
        elif lOp == 2:
            localMem.insertChar(globalMem.getInt(quad.left_operand), quad.left_operand)
        
def add(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp + rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)

def subtract(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp - rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)

def multiply(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp * rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)

def divide(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp / rOp
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)

def greaterThan(quad):
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp > rOp
    tempMem.insertInt(result, quad.result)

def lessThan(quad):
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = lOp < rOp
    tempMem.insertInt(result, quad.result)

def notEqual(quad):
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp != rOp)
    tempMem.insertInt(result, quad.result)

def equals(quad):
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp == rOp)
    tempMem.insertInt(result, quad.result)

def orOp(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp or rOp)
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def andOp(quad):
    res_address = quad.result // 1000
    if quad.left_operand >= 9000:
        lOp = cstMemMap[quad.left_operand]
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if quad.right_operand >= 9000:
        rOp = cstMemMap[quad.right_operand]
    else:
        rOp = getValueFromAddress(quad.right_operand)
    result = (lOp and rOp)
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    if res_address == 7:
        tempMem.insertFloat(result, quad)
    if res_address == 8:
        tempMem.insertChar(result, res_address)

def read(quad):
    address = quad.result // 1000
    input_val = input()
    if re.match(r'[0-9]+', input_val):
        input_val = int(input_val)
        if address == 0:
            globalMem.insertInt(input_val, quad.result)
        elif address == 3:
            localMem.insertInt(input_val, quad.result)
    elif re.match(r'[0-9]+\.[0-9]+', input_val):
        input_val = float(input_val)
        if address == 1:
            globalMem.insertFloat(input_val, quad.result)
        elif address == 4:
            localMem.insertFloat(input_val, quad.result)
    elif re.match(r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')', input_val):
        input_val = input_val[1]
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    elif re.match(r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')', input_val):
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    else:
        input_val = input_val[0]
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    
def printScreen(quad):
    if quad.result >= 9000:
        print(cstMemMap[quad.result])
    else:
        print(getValueFromAddress(quad.result))

def endFunc(quad):
    pass

def gotof(quad):
    pass

def goto(quad):
    pass

def gosub(quad):
    pass

def era(quad):
    pass

def param(quad):
    pass
    