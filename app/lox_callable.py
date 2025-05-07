import time
from typing import Protocol, List, Any
from typing import Protocol, runtime_checkable

@runtime_checkable
class LoxCallable(Protocol):
    def call(self, interpreter, arguments: List[Any]) -> Any:
        ...

    def arity(self) -> int:
        ...


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: List[Any]) -> Any:
        return time.time()

    def __str__(self) -> str:
        return "<native fn>"