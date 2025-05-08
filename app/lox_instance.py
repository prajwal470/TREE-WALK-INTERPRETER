

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}


    def get(self, name_token):
        if name_token.lexeme in self.fields:
            return self.fields[name_token.lexeme]
        
        method = self.klass.find_method(name_token.lexeme)
        if method:
            return method.bind(self)

        raise RuntimeError(name_token, f"Undefined property '{name_token.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"
    
    
   