from dataclasses import dataclass
from enum import StrEnum

from .minion import Minion


class Player(StrEnum):
    ME = "me"
    ENEMY = "enemy"

    def __invert__(self):
        return Player.ENEMY if self == Player.ME else Player.ME


@dataclass
class Board:
    my_minions: list[Minion]
    enemy_minions: list[Minion]
    last_turn: Player | None = None

    @staticmethod
    def from_minions(my_minions: list[Minion], enemy_minions: list[Minion]) -> "Board":
        return Board(my_minions, enemy_minions)
