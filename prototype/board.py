from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum

from . import event
from .effects.base import BaseEffect
from .minion import Minion


class Player(StrEnum):
    Me = "me"
    Enemy = "enemy"

    def __str__(self):
        return self.value.ljust(5)

    def __invert__(self):
        return Player.Enemy if self == Player.Me else Player.Me


@dataclass
class BoardMetadata:
    blood_gems: tuple[int, int] = (1, 1)
    beetles: tuple[int, int] = (2, 2)


@dataclass
class Board:
    my_minions: list[Minion]
    enemy_minions: list[Minion]

    event_handlers: defaultdict[event.Event, list[BaseEffect]] = field(
        default_factory=defaultdict
    )

    last_turn: Player | None = None
    metadata: BoardMetadata = field(default_factory=BoardMetadata)

    @staticmethod
    def from_minions(my_minions: list[Minion], enemy_minions: list[Minion]) -> "Board":
        return Board(my_minions, enemy_minions)
