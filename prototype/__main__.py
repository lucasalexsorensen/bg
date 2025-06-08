from .minion import Minion
from .simulator import simulate_combat


def main():
    my_minions = [Minion.from_id(116734)]
    enemy_minions = [Minion.from_id(119994), Minion.from_id(98582)]

    print(simulate_combat(my_minions, enemy_minions))


if __name__ == "__main__":
    main()
