import pytest

from ..minion import Minion
from ..simulator import Simulator


class TestSimulator:
    @pytest.mark.parametrize(
        ("my_minions", "enemy_minions"),
        [
            (
                [Minion.from_name("dune dweller")],
                [Minion.from_name("surfing sylvar"), Minion.from_name("lullabot")],
            ),
            ([Minion.from_name("buzzing vermin")], [Minion.from_name("lullabot")]),
        ],
    )
    def test_guaranteed_draws(
        self, my_minions: list[Minion], enemy_minions: list[Minion]
    ):
        assert Simulator(my_minions, enemy_minions).simulate() == 0

    @pytest.mark.parametrize(
        ("my_minions", "enemy_minions"),
        [],
    )
    def test_guaranteed_wins(
        self, my_minions: list[Minion], enemy_minions: list[Minion]
    ):
        assert Simulator(my_minions, enemy_minions).simulate() == 1

    @pytest.mark.parametrize(
        ("my_minions", "enemy_minions"),
        [],
    )
    def test_guaranteed_losses(
        self, my_minions: list[Minion], enemy_minions: list[Minion]
    ):
        pass
