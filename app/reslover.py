from lox import *
from typing import List, Dict
from token_type import TokenType , Token
from enum import Enum
from lox_stmt import *
from lox_expression import *
from lox import Lox
from _return import Return






class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1
    INITIALIZER = 2
    METHOD = 3

class ClassType(Enum):
    NONE = 0
    CLASS = 1
    SUBCLASS = 2



class Resolver(Expr, Stmt):

    
    # 

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes: List[Dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.currentClass = ClassType.NONE

    def visitBlockStmt(self, stmt: Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None
    
    def visit_class_stmt(self, stmt: Class):

        enclosing_class = self.currentClass
        self.currentClass = ClassType.CLASS


        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                Lox.error(stmt.superclass.name, "A class can't inherit from itself.")
            self.resolve_expr(stmt.superclass)
            
        self.begin_scope()

        self.scopes[-1]["this"] = True


        for method in stmt.methods:
            declaration = FunctionType.METHOD

            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER

            self.resolve_function(method, declaration)

        self.end_scope()
        self.currentClass = enclosing_class
        return None

    def resolve(self, statements: List[Stmt]):
        for stmt in statements:
            self.resolve_stmt(stmt)
            

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolve_expr(self, expr: Expr):
        expr.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    # def declare(self, name: Token):
    #     if not self.scopes:
    #         return
    #     scope = self.scopes[-1]
    #     scope[name.lexeme] = False

    def declare(self, name: Token):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            Lox.error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def visit_var_stmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)
        return None

    def visit_variable_expr(self, expr: Variable):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            Lox.error(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
        return None

    def resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def visit_assign_expr(self, expr: Assign):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    # def visitFunctionStmt(self, stmt: Function):
    #     self.declare(stmt.name)
    #     self.define(stmt.name)
    #     self.resolve_function(stmt)
    #     return None
    

    def visit_function_stmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    
    def resolve_function(self, function: Function, type_: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type_

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function




    def visit_expression_stmt(self, stmt: ExpressionStmt):
        self.resolve_expr(stmt.expression)
        return None

    def visit_if_stmt(self, stmt: If):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch:
            self.resolve_stmt(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt: PrintStmt):
        self.resolve_expr(stmt.expression)
        return None

    # def visitReturnStmt(self, stmt: Return):
    #     if stmt.value is not None:
    #         self.resolve_expr(stmt.value)
    #     return None
    
    def visit_return_stmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            Lox.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value:

            if self.current_function == FunctionType.INITIALIZER:
                Lox.error(stmt.keyword, "Can't return a value from an initializer.")

            self.resolve_expr(stmt.value)
        return None

    def visit_while_stmt(self, stmt: While):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)
        return None

    def visit_binary_expr(self, expr: Binary):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None

    def visit_call_expr(self, expr: Call):
        self.resolve_expr(expr.callee)
        for arg in expr.arguments:
            self.resolve_expr(arg)
        return None
    
    def visit_get_expr(self, expr: Get):
        self.resolve_expr(expr.object)
        return None

    def visit_grouping_expr(self, expr: Grouping):
        self.resolve_expr(expr.expression)
        return None

    def visit_literal_expr(self, expr: Literal):
        return None

    def visit_logical_expr(self, expr: Logical):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None
    
    def visit_set_expr(self, expr: Set):
        self.resolve_expr(expr.value)
        self.resolve_expr(expr.object)
        return None

    def visit_this_expr(self, expr: This):
        self.resolve_local(expr, expr.keyword)

        if self.currentClass == ClassType.NONE:
            Lox.error(expr.keyword, "Can't use 'this' outside of a class.")
       


        return None
   



    def visit_unary_expr(self, expr: Unary):
        self.resolve_expr(expr.right)
        return None