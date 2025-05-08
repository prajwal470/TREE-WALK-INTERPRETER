from token_type import TokenType , Token
from lox_expression import Expr

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