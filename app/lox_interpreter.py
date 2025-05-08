from lox_environment import Environment
from token_type import TokenType , Token
from lox_callable import *
from lox_function import LoxFunction
from lox_class import LoxClass
from _return import Return
from lox import *
from lox_stmt import *
from lox_expression import *
from reslover import Resolver
from lox_instance import LoxInstance



class Interpreter(Stmt.Visitor, Expr.Visitor):

    def __init__(self):
        self.environment = Environment()
        self.locals: dict[Expr, int] = {}
        self.globals = Environment()
        self.environment = self.globals
        self.methods = {}
        # Define native function "clock"
        self.globals.define("clock", Clock())


    def interpret(self, statements):
        try:
            for statement in statements:
                if statement is not None:
                    self.execute(statement)
        except RuntimeError as error:
            print(f"Runtime error: {error}")

    def execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth
 
    # --- Statement Visitors ---
    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            return self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            return self.execute(stmt.else_branch)
        return None

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None
    
    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)
    
    # def visit_class_stmt(self, stmt):
    #     self.environment.define(stmt.name.lexeme, None)

    #     klass = LoxClass(stmt.name.lexeme)
    #     self.environment.assign(stmt.name, klass)

    #     return None
    
    def visit_class_stmt(self, stmt):
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            function = LoxFunction(method, self.environment, method.name.lexeme == "init")
            methods[method.name.lexeme] = function

        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if stmt.superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)
        return None

    


    

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None
    

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:  # AND
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)
    
    def visit_set_expr(self, expr):
        object = self.evaluate(expr.object)

        if isinstance(object, LoxInstance):
            value = self.evaluate(expr.value)
            object.set(expr.name, value)
            return value

        raise RuntimeError(expr.name, "Only instances have fields.")
    
    def visit_function_stmt(self, stmt):
        function = LoxFunction(stmt,self.environment , False)
        self.environment.define(stmt.name.lexeme, function)


        return None



    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # --- Expression Visitors ---
    def evaluate(self, expr):
        return expr.accept(self)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == 'MINUS':
            self.check_number_operand(expr.operator, right)
            return -float(right)
        if expr.operator.type == 'BANG':
            return not self.is_truthy(right)

        return None  # Unreachable
    
    def visit_variable_expr(self, expr):
        # return self.environment.get(expr.name)
        return self.look_up_variable(expr.name, expr)
    
    def look_up_variable(self, name: Token, expr: Expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == 'PLUS':
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError("Operands must be two numbers or two strings.")

        if expr.operator.type == 'MINUS':
            self.check_number_operands(expr.operator, left, right)
            return left - right

        if expr.operator.type == 'STAR':
            self.check_number_operands(expr.operator, left, right)
            return left * right

        if expr.operator.type == 'SLASH':
            self.check_number_operands(expr.operator, left, right)
            if right == 0:
                raise RuntimeError("Division by zero.")
            return left / right

        if expr.operator.type == 'GREATER':
            self.check_number_operands(expr.operator, left, right)
            return left > right

        if expr.operator.type == 'GREATER_EQUAL':
            self.check_number_operands(expr.operator, left, right)
            return left >= right

        if expr.operator.type == 'LESS':
            self.check_number_operands(expr.operator, left, right)
            return left < right

        if expr.operator.type == 'LESS_EQUAL':
            self.check_number_operands(expr.operator, left, right)
            return left <= right

        if expr.operator.type == 'BANG_EQUAL':
            return not self.is_equal(left, right)

        if expr.operator.type == 'EQUAL_EQUAL':
            return self.is_equal(left, right)

        return None  # Unreachable
    
    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")

        if len(arguments) != callee.arity():
            raise RuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")

        return callee.call(self, arguments)
    
    def visit_get_expr(self , expr):
        object = self.evaluate(expr.object)
        if isinstance(object, LoxInstance):
            return object.get(expr.name)
        raise RuntimeError(expr.name, "Only instances have properties.")
        
    def visit_this_expr(self, expr):
        return self.look_up_variable(expr.keyword, expr)


    # --- Helper Methods ---
    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b):
        return a == b

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(f"Operand must be a number: {operator}")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(f"Operands must be numbers: {operator}")

    def stringify(self, value):
        if value is None:
            return "nil"
        elif isinstance(value, bool):
            return "true" if value else "false"
        return str(value)
    
#   def stringify(self, obj):
#         if obj is None:
#             return "nil"
#         if isinstance(obj, float):
#             text = str(obj)
#             if text.endswith(".0"):
#                 text = text[:-2]
#             return text
#         return str(obj)