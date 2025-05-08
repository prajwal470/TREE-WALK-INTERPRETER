from abc import ABC, abstractmethod

class Expr:
    
    class Visitor:
        @abstractmethod
        def visit_binary_expr(self, expr): pass
        @abstractmethod
        def visit_grouping_expr(self, expr): pass
        @abstractmethod
        def visit_literal_expr(self, expr): pass
        @abstractmethod
        def visit_unary_expr(self, expr): pass
        @abstractmethod
        def visit_variable_expr(self, expr): pass
        @abstractmethod
        def visit_assign_expr(self, expr): pass
        @abstractmethod
        def visit_logical_expr(self,expr): pass
        @abstractmethod
        def visit_call_expr(self, expr): pass
        @abstractmethod
        def visit_this_expr(self, expr): pass



    def accept(self, visitor):
        pass

# stamtent visitor calss    


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)
    
    # def __str__(self):
    #     return f"Binary({self.left}, {self.operator}, {self.right})"

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

    # def __str__(self):
    #     return f"Binary({self.left}, {self.operator}, {self.right})"

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)
    
    # def __str__(self):
    #     return f"{self.value}"

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)
    
    # def __str__(self):
    #     return f"{self.value}"

class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)



class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name  # Token
        self.value = value  # Expr
    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)
    
class Get(Expr):
    def __init__(self, object, name):
        self.object = object  # Expr
        self.name = name      # Token

    def accept(self, visitor):
        return visitor.visit_get_expr(self)


class Set(Expr):
    def __init__(self, object, name , value):
        self.object = object  # Expr
        self.name = name      # Token
        self.value = value # Expr
    
    def accept(self, visitor):
        return visitor.visit_set_expr(self)
    
class This(Expr):
    def __init__(self, keyword):
        self.keyword = keyword  # Token

    def accept(self, visitor):
        return visitor.visit_this_expr(self)
    
