from .minion import Minion
from .simulator import Simulator


def main():
    my_minions = [Minion.from_id(116734)]
    enemy_minions = [Minion.from_id(119994), Minion.from_id(98582)]

    simulator = Simulator(my_minions, enemy_minions)
    print(simulator.simulate())


if __name__ == "__main__":
    main()
