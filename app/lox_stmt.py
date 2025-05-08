from abc import abstractmethod

class Stmt:
    class Visitor:
        @abstractmethod
        def visit_print_stmt(self, stmt): pass
        @abstractmethod
        def visit_expression_stmt(self, stmt): pass
        @abstractmethod
        def visit_var_stmt(self, stmt): pass
        @abstractmethod
        def visit_block_stmt(self, stmt): pass
        @abstractmethod
        def visit_if_stmt(self, stmt): pass
        @abstractmethod
        def visit_while_stmt(self, stmt): pass
        @abstractmethod
        def visit_function_stmt(self, stmt): pass
        @abstractmethod
        def visit_return_stmt(self, stmt): pass
        @abstractmethod
        def visit_class_stmt(self, stmt): pass
        @abstractmethod
        def visit_resolve_stmt(self, stmt): pass

        def accept(self, visitor):
            pass


class Class(Stmt):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass  # Expr.Variable or None
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)
        
class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class Var(Stmt): 
    def __init__(self, name, initializer):
        self.name = name      # a Token
        self.initializer = initializer  # an Expr
    def accept(self, visitor):
        return visitor.visit_var_stmt(self)
    

class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class While(Stmt):
    
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


class Function(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)


class ReturnStmt(Stmt):
    def __init__(self , keyword, value ):
        self.keyword = keyword
        self.value  = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


class Class(Stmt):
    def __init__(self, name, superclass, methods ):
        self.name = name     
        self.superclass = superclass   # Token
        self.methods = methods  
          # Expr.Variable or None

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)

# class resolve_stmt(Stmt):
#     def __init__(self, name):
#         self.name = name

#     def accept(self, visitor):
#         return visitor.visit_resolve_stmt(self)