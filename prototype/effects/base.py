from abc import ABC, abstractmethod

from ..board import Board


class BaseEffect(ABC):
    @abstractmethod
    def apply(self, board: Board) -> None:
        pass
