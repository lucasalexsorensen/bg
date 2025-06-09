from dataclasses import dataclass, field
from typing import Annotated, Literal, Union
from uuid import UUID

from prototype.player import Player


@dataclass
class MinionReference:
    uuid: UUID
    index: int


@dataclass
class CombatStarted:
    type: Literal["combat_started"] = "combat_started"


@dataclass
class MinionDied:
    player: Player
    minion_uuid: UUID
    minion_index: int
    type: Literal["minion_died"] = "minion_died"


@dataclass
class MinionSummoned:
    player: Player
    minion_uuid: UUID
    minion_index: int
    type: Literal["minion_summoned"] = "minion_summoned"


@dataclass
class MinionBuffed:
    player: Player
    minion_uuid: UUID
    type: Literal["minion_buffed"] = "minion_buffed"


@dataclass
class PreAttack:
    player: Player
    attacker_uuid: UUID
    target_uuid: UUID
    type: Literal["pre_attack"] = "pre_attack"


@dataclass
class PostAttack:
    player: Player
    attacker_uuid: UUID
    target_uuid: UUID
    type: Literal["post_attack"] = "post_attack"


@dataclass
class DeathrattleTriggered:
    minion_uuid: UUID
    type: Literal["deathrattle_triggered"] = "deathrattle_triggered"


@dataclass
class BattlecryTriggered:
    minion_uuid: UUID
    type: Literal["battlecry_triggered"] = "battlecry_triggered"


@dataclass
class SpaceAvailable:
    type: Literal["space_available"] = "space_available"


@dataclass
class DivineShieldLost:
    minion_uuid: UUID
    type: Literal["divine_shield_lost"] = "divine_shield_lost"


Event = Union[
    CombatStarted,
    MinionDied,
    MinionSummoned,
    MinionBuffed,
    PreAttack,
    PostAttack,
    DeathrattleTriggered,
    BattlecryTriggered,
    SpaceAvailable,
    DivineShieldLost,
]
