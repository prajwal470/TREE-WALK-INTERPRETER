
from token_type import TokenType , Token


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing  # Link to outer (enclosing) environment
        self.values = {}            # Dictionary to hold variable bindings
        self.Token = None  # Placeholder for the token type, if needed

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment
    
    def get(self, name_token):
        name = name_token.lexeme
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name_token)
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")

    def assign(self, name_token, value):
        name = name_token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name_token, value)
            return
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")
    
    def get_at(self, distance: int, name: str):
        return self.ancestor(distance).values[name]
    
    def assign_at(self, distance: int, name: Token, value: object):
        self.ancestor(distance).values[name.lexeme] = value
