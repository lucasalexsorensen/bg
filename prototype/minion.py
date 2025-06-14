from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Callable
from uuid import UUID, uuid4

from .dataset import Dataset


class Keyword(StrEnum):
    """
    A Bonus Keyword is one of 6 keywords used in Battlegrounds:
      Shield, Reborn, Stealth, Taunt, Venomous, or Windfury.
    """

    DivineShield = "divine_shield"
    Reborn = "reborn"
    Stealth = "stealth"
    Taunt = "taunt"
    Venomous = "venomous"
    Windfury = "windfury"


@dataclass
class Minion:
    uuid: UUID
    id: int
    name: str
    attack: int
    health: int
    keywords: set[Keyword] = field(default_factory=set)
    attack_count: int = 0
    effects: defaultdict[str, list[str]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Minion) and self.uuid == other.uuid

    def __str__(self):
        return f"{self.name} ({self.attack}/{self.health})"

    @property
    def taunt(self) -> bool:
        return Keyword.Taunt in self.keywords

    @property
    def divine_shield(self) -> bool:
        return Keyword.DivineShield in self.keywords

    @property
    def windfury(self) -> bool:
        return Keyword.Windfury in self.keywords

    @property
    def venomous(self) -> bool:
        return Keyword.Venomous in self.keywords

    @property
    def reborn(self) -> bool:
        return Keyword.Reborn in self.keywords

    @property
    def stealth(self) -> bool:
        return Keyword.Stealth in self.keywords

    @staticmethod
    def from_id(
        id: int, health: int | None = None, attack: int | None = None
    ) -> "Minion":
        m = Dataset().get_by_id(id)
        return Minion(
            uuid=uuid4(),
            id=m["id"],
            name=m["name"],
            attack=m["attack"] if attack is None else attack,
            health=m["health"] if health is None else health,
            effects=defaultdict(list) | effects_from_name(m["name"]),
        )

    @staticmethod
    def from_name(name: str, **kwargs) -> "Minion":
        m = Dataset().get_by_name(name)
        return Minion.from_id(m["id"], **kwargs)

    @staticmethod
    def custom(name: str, health: int, attack: int):
        return Minion(
            id=0,
            uuid=uuid4(),
            name=name,
            health=health,
            attack=attack,
        )


def effects_from_name(name: str) -> dict[str, list[str]]:
    match name:
        case "Buzzing Vermin":
            return {"deathrattle": ["summon_beetle"]}
        case "Manasaber":
            return {"deathrattle": ["summon_cublings"]}
        case "Dozy Whelp":
            return {"pre_attack": ["dozy_whelp"]}
        case "Misfit Dragonling":
            return {"start_of_combat": ["misfit_dragonling"]}
        case "Cord Puller":
            return {"deathrattle": ["summon_microbot"]}
        case "Harmless Bonehead":
            return {"deathrattle": ["summon_skeletons"]}
        case _:
            return {}
