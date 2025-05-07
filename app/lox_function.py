from env import Environment
from typing import List
from lox_callable import LoxCallable
from _return import Return


# class LoxFunction(Function):
#     def __init__(self, declaration):
#         self.declaration = declaration

#     def call(self, Interpreter, arguments):
#         environment = Environment(Interpreter.globals)
#         for i in range(len(self.declaration.params)):
#             param_name = self.declaration.params[i].lexeme
#             environment.define(param_name, arguments[i])

#         Interpreter.execute_block(self.declaration.body, environment)
#         return None

#     def arity(self):
#         return len(self.declaration.params)

#     def __str__(self):
#         return f"<fn {self.declaration.name.lexeme}>"
    

class LoxFunction(LoxCallable):
    def __init__(self, declaration , closure):
        self.declaration = declaration  # Stmt.Function instance
        self.closure = closure  # Environment to capture variables from the enclosing scope


    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme,
                               arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"