from .board import Board, Player
from .minion import Minion


class TestPlayer:
    def test_player(self):
        assert Player.ME == ~Player.ENEMY
        assert Player.ENEMY == ~Player.ME


class TestBoard:
    def test_evaluate(self):
        board = Board.from_minions(
            [Minion.from_id(116734)], [Minion.from_id(119994), Minion.from_id(98582)]
        )
