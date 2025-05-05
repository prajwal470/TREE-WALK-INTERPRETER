from abc import abstractmethod
import sys
from typing import List
from env import Environment

class TokenType:
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    SLASH = 'SLASH'
    STAR = 'STAR'

    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'

    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    AND = 'AND'
    CLASS = 'CLASS'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    NIL = 'NIL'
    OR = 'OR'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'

    EOF = 'EOF'

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

    def __repr__(self):
        return self.__str__()

class Lox:
    hadError = False

    @staticmethod
    def error(token, message):
        if token.type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox.hadError = True

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


class AstPrinter(Expr.Visitor):
    def print(self, expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs):
        parts = [name]
        for expr in exprs:
            parts.append(expr.accept(self))
        return "(" + " ".join(parts) + ")"

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

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


# class Print(Stmt):
#     def __init__(self, expression):
#         self.expression = expression

#     def accept(self, visitor):
#         return visitor.visit_print_stmt(self)





class ParseError(RuntimeError):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # def parse(self):
    #     try:
    #         return self.expression()
    #     except ParseError:
    #         return None
    
    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements
    
    # def parse(self):
    #     statements = []
    #     while not self.is_at_end():
    #         stmt = self.statement()
    #         if stmt is not None:
    #             statements.append(declaration());
    #     return statements

    def declaration(self):
        try:
            if self.match('VAR'):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None
        
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ):
                return

            self.advance()



    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.equality()

        if self.match("EQUAL"):  # Check for '=' assignment
            equals = self.previous()
            value = self.assignment()  # Get the right side expression

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)  # Return an assignment expression
            else:
                raise RuntimeError(f"Invalid assignment target: {equals}")
        
        return expr

    def block(self):
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expression_statement()
    
    

    def if_statement(self):
        self.consume('LEFT_PAREN', "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume('RIGHT_PAREN', "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match('ELSE'):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)


    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)
    
    def var_declaration(self):
        name = self.consume('IDENTIFIER', "Expect variable name.")

        initializer = None
        if self.match('EQUAL'):
            initializer = self.expression()

        self.consume('SEMICOLON', "Expect ';' after variable declaration.")
        return Var(name, initializer)
        
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)
        
    
    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match('LEFT_BRACE'):
            return Block(self.block())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
 

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        Lox.error(token, message)
        return ParseError()

class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        if c == '(': self.add_token(TokenType.LEFT_PAREN)
        elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self.add_token(TokenType.LEFT_BRACE)
        elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == ';': self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in (' ', '\r', '\t'):
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            print(f"[line {self.line}] Unexpected character '{c}'", file=sys.stderr)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected):
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            print(f"[line {self.line}] Unterminated string.", file=sys.stderr)
            return

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start:self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)



    
class Interpreter(Stmt.Visitor, Expr.Visitor):

    def __init__(self):
        self.environment = Environment()


    def interpret(self, statements):
        try:
            for statement in statements:
                if statement is not None:
                    self.execute(statement)
        except RuntimeError as error:
            print(f"Runtime error: {error}")

    def execute(self, stmt):
        stmt.accept(self)

 
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

    
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None
    

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
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
        return self.environment.get(expr.name)

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
    
    
    


