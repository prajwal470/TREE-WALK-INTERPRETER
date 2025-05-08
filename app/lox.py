from abc import abstractmethod
import sys
from token_type import TokenType , Token
from lox_expression import Expr


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




    


