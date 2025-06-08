from ..board import Board
from ..minion import Minion
from .base import BaseEffect


class SummonBeetle(BaseEffect):
    def apply(self, board: Board) -> None:
        if len(board.my_minions) >= 7:
            return
        health, attack = board.metadata.beetles
        beetle = Minion.custom(name="Spawned Beetle", health=health, attack=attack)
        board.my_minions.insert(0, beetle)


class SummonCubs(BaseEffect):
    def apply(self, board: Board) -> None:
        cubs = [Minion.custom(name="Cub", health=0, attack=0) for _ in range(2)]
        for cub in cubs:
            if len(board.my_minions) >= 7:
                break
            board.my_minions.insert(0, cub)
