from lox_expression import *
from lox_stmt import *
from token_type import *
from lox import Lox


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
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None
        

    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = Variable(self.previous())  # Expr.Variable

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        
        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        
        return Class(name, superclass, methods)
        
    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
                if not self.match(TokenType.COMMA):
                    break

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect "'{'" before {kind} body.")
        body = self.block()
        return Function(name, parameters, body)
    
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
            elif isinstance(expr, Get):
                return Set(expr.object, expr.name, value)
    
            else:
                raise RuntimeError(f"Invalid assignment target: {equals}")
        
        return expr
    
    def or_(self):
        expr = self.and_()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)

        return expr

    def and_(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

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
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        

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
    

    def while_statement(self):
        self.consume('LEFT_PAREN', "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume('RIGHT_PAREN', "Expect ')' after condition.")

        body = self.statement()

        return While(condition, body)
    
    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        # --- Initializer ---
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        # --- Condition ---
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        # --- Increment ---
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        # --- Body ---
        body = self.statement()

        # Desugar: Add increment after the body
        if increment is not None:
            body = Block([
                body,
                ExpressionStmt(increment)
            ])

        # Desugar: Use true if no condition
        if condition is None:
            condition = Literal(True)

        body = While(condition, body)

        # Desugar: Wrap initializer before the loop
        if initializer is not None:
            body = Block([initializer, body])

        return body




    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)
    

    def return_statement(self):
        
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(keyword, value)

    
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

        return self.call()
    
    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = Get(expr, name)
            else:
                break
        return expr
    
    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee, paren, arguments)


    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT , "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Super(keyword , method)

        if self.match(TokenType.THIS):
            return This(self.previous())


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