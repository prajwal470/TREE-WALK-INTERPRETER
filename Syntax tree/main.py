from expr import Binary, Unary, Literal, Grouping
from token_1 import Token
from type_token import TokenType
from ast_printer import AstPrinter

# Build the expression: (-123) * (45.67)
expression = Binary(
    left=Unary(
        operator=Token(TokenType.MINUS, "-", None, 1),
        right=Literal(123)
    ),
    operator=Token(TokenType.STAR, "*", None, 1),
    right=Grouping(
        expression=Literal(45.67)
    )
)

printer = AstPrinter()
print(printer.print(expression))