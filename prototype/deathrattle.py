from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class SummonBeetle:
    type: Literal["summon_beetle"] = "summon_beetle"


@dataclass
class SummonCublings:
    type: Literal["summon_cublings"] = "summon_cublings"


type Deathrattle = Union[SummonBeetle, SummonCublings]
