#Definicion de PDTs
type_dict = {
    'void' : 0,
    'boolean' : 1,
    'int' : 2,
    'decimal' : 3,
    'string' : 4,
}
inv_type_dict = {
    v: k for k, v in type_dict.items()
}

#Helper classes
class Stack(object):
    def __init__(self):
        self.values = []

    def isEmpty(self):
        return self.values == []
    
    def push(self, value):
        self.values.append(value)
    
    def pop(self):
        if(len(self.values) > 0):
            return self.values.pop()
        else:
            print("Stack vacio")
    
    def peek(self):
        if(len(self.values) == 0):
            return None
        else:
            return self.values[len(self.values)-1]
    
    def size(self):
        return len(self.values)
    
    def pprint(self):
        print self.values

    def inStack(self,var_name):
        return var_name in self.values

    
class Queue(object):

     def __init__(self):
        self.values = []

    def isEmpty(self):
        return self.values == []
    
    def pprint(self):
        print self.values

    def size(self):
        return len(self.values)

    def enqueue(self,value):
        self.values.insert(0,value)

    def dequeue(self):
        if(len(self.values) > 0 ):
            return self.values.pop()
        else:
            print("Queue vacia")

    def peek(self):
        return self.values[len(self.values)-1]

    def inQueue(self, var_name):
        return var_name in self.values