from .minion import Minion
from .simulator import Simulator


def main():
    my_minions = [Minion.from_name("buzzing vermin")]
    enemy_minions = [Minion.from_name("lullabot")]

    simulator = Simulator(my_minions, enemy_minions)
    print(simulator.simulate())


if __name__ == "__main__":
    main()
