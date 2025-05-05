class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing  # Link to outer (enclosing) environment
        self.values = {}            # Dictionary to hold variable bindings

    def define(self, name, value):
        self.values[name] = value

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
