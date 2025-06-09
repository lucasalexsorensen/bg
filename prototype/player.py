from enum import StrEnum


class Player(StrEnum):
    A = "A"
    B = "B"

    def __repr__(self):
        return f"Player.{self.value}"

    def __invert__(self):
        return Player.B if self == Player.A else Player.A
