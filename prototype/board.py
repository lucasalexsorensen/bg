from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Self

from .minion import Minion
from .player import Player


@dataclass
class BoardMetadata:
    blood_gems: tuple[int, int] = (1, 1)
    beetles: tuple[int, int] = (2, 2)
    elemental_bonus: tuple[int, int] = (0, 0)


type Effect = Callable[[], list[str]]


@dataclass
class Board:
    minions: dict[Player, list[Minion]]
    metadata: dict[Player, BoardMetadata]
    dead_minions: dict[Player, set[Minion]]
    last_turn: Player | None

    @staticmethod
    def from_minions(a: list[Minion], b: list[Minion]) -> "Board":
        return Board(
            minions={Player.A: a, Player.B: b},
            metadata={Player.A: BoardMetadata(), Player.B: BoardMetadata()},
            dead_minions={Player.A: set(), Player.B: set()},
            last_turn=None,
        )

    def apply_effect(self, player: Player, effect: Effect) -> None:
        pass

    def has_space(self, player: Player) -> bool:
        return len(self.minions[player]) < 7

    def process_effect(self, player: Player | None, effect: str) -> list[str]:
        match effect:
            case "summon_beetle":
                if not self.has_space(player):
                    return []
                pm = self.metadata[player]
                beetle = Minion.custom("Nick Noren", pm.beetles[0], pm.beetles[1])
                self.minions[player].insert(0, beetle)
                return ["minion_summoned"]
        raise ValueError(f"Unknown effect: {effect}")
