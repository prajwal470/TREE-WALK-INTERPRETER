from lox_callable import LoxCallable
from lox_instance import LoxInstance



class LoxClass(LoxCallable):

    
        
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)



        return instance

    def arity(self):
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def __str__(self):
        return self.name
    
    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.find_method(name)
        return None
