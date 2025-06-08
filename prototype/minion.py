import random
from dataclasses import dataclass
from uuid import UUID, uuid4

from .dataset import Dataset


@dataclass
class Minion:
    uuid: UUID
    id: int
    name: str
    attack: int
    health: int
    taunt: bool = False
    divine_shield: bool = False
    has_attacked: bool = False
    attack_count: int = 0

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Minion) and self.uuid == other.uuid

    def __str__(self):
        return f"{self.name} ({self.attack}/{self.health})"

    @staticmethod
    def from_id(id: int) -> "Minion":
        m = Dataset().get_by_id(id)
        return Minion(
            uuid=uuid4(),
            id=m["id"],
            name=m["name"],
            attack=m["attack"],
            health=m["health"],
        )
