from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol
from token_1 import Token


class Expr(ABC):
    def accept(self, visitor):
        raise NotImplementedError()


class ExprVisitor(Protocol):
    def visit_binary_expr(self, expr: 'Binary') -> Any:
        ...
    def visit_grouping_expr(self, expr: 'Grouping') -> Any:
        ...
    def visit_literal_expr(self, expr: 'Literal') -> Any:
        ...
    def visit_unary_expr(self, expr: 'Unary') -> Any:
        ...

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)

