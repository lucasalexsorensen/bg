from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from .board import Player
from .minion import Minion


class CombatStarted(BaseModel):
    type: Literal["combat_started"] = "combat_started"


class MinionDied(BaseModel):
    type: Literal["minion_died"] = "minion_died"
    minion: Minion
    owner: Player


class MinionSummoned(BaseModel):
    type: Literal["minion_summoned"] = "minion_summoned"
    minion: Minion
    owner: Player


class MinionBuffed(BaseModel):
    type: Literal["minion_buffed"] = "minion_buffed"
    minion: Minion
    owner: Player


class PreAttack(BaseModel):
    type: Literal["pre_attack"] = "pre_attack"
    attacker: Minion
    target: Minion


class PostAttack(BaseModel):
    type: Literal["post_attack"] = "post_attack"
    attacker: Minion
    target: Minion


class DeathrattleTriggered(BaseModel):
    type: Literal["deathrattle_triggered"] = "deathrattle_triggered"
    minion: Minion
    owner: Player


class BattlecryTriggered(BaseModel):
    type: Literal["battlecry_triggered"] = "battlecry_triggered"
    minion: Minion
    owner: Player


class SpaceAvailable(BaseModel):
    type: Literal["space_available"] = "space_available"


class DivineShieldLost(BaseModel):
    type: Literal["divine_shield_lost"] = "divine_shield_lost"
    minion: Minion
    owner: Player


Event = Annotated[
    Union[
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
    ],
    Field(discriminator="type"),
]
