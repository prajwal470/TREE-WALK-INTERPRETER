from lox_environment import Environment
from typing import List
from lox_callable import LoxCallable
from _return import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.isInitializer:
                return self.closure.get_at(0, "this")
            return return_value.value

        if self.isInitializer:
            return self.closure.get_at(0, "this")
        return None

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.isInitializer)

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"