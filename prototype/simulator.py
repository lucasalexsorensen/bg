import random
from collections import deque
from copy import deepcopy

from loguru import logger
from loguru._logger import Logger  # for type hinting only

from . import event
from .board import Board, Player
from .minion import Minion

random.seed(1337)

logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="{level.icon} {time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | Turn: {extra[turn]!s} | {message}",
    level="INFO",
    filter=lambda record: record["extra"].setdefault("turn", "N/A"),
)


class Simulator:
    def __init__(self, my_minions: list[Minion], enemy_minions: list[Minion]):
        self.logger = logger.bind(turn=None)
        self.board = Board(
            my_minions=deepcopy(my_minions),
            enemy_minions=deepcopy(enemy_minions),
        )
        self.last_turn: Player | None = None

    def perform_attack(
        self,
        attacker: Minion,
        attacker_minions: list[Minion],
        target: Minion,
        target_minions: list[Minion],
    ) -> None:
        self.logger.info(f"{attacker} attacks {target}")
        self.handle_event(event.PreAttack(attacker=attacker, target=target))

        # do the trade
        attacker.health -= target.attack
        target.health -= attacker.attack
        attacker.attack_count += 1
        self.handle_event(event.PostAttack(attacker=attacker, target=target))

        # check for target death
        if target.health <= 0:
            self.logger.info(f"{target} dies")
            target_minions.remove(target)
            target_player = (
                Player.Me if target_minions is self.board.my_minions else Player.Enemy
            )
            self.handle_event(event.MinionDied(minion=target, owner=target_player))

        # check for attacker death
        if attacker.health <= 0:
            self.logger.info(f"{attacker} dies")
            attacker_minions.remove(attacker)
            attacker_player = (
                Player.Me if attacker_minions is self.board.my_minions else Player.Enemy
            )
            self.handle_event(event.MinionDied(minion=attacker, owner=attacker_player))

    def simulate(self) -> int:
        winner: Player | None = None

        while True:
            # 1. determine whose turn it is
            turn = self.determine_turn()
            self.logger = self.logger.bind(turn=turn)
            self.logger.info(f"Turn: {turn}")

            attacker_minions, target_minions = (
                (self.board.my_minions, self.board.enemy_minions)
                if turn == Player.Me
                else (self.board.enemy_minions, self.board.my_minions)
            )

            # 2. determine which minion will be attacking
            attacker = self.determine_attacker(attacker_minions)

            # 3. determine which minion will be targeted
            target = self.determine_target(target_minions)

            match (attacker, target):
                case (None, None):
                    self.logger.info("No attacker or target found - draw ")
                    winner = None
                    break
                case (None, _):
                    self.logger.info(f"No attacker found - winner is {turn}")
                    winner = turn
                    break
                case (_, None):
                    self.logger.info(f"No target found - winner is {turn}")
                    winner = ~turn
                    break

            # 4. perform the attack
            self.perform_attack(attacker, attacker_minions, target, target_minions)

            # 5. update the board
            self.last_turn = turn

        match winner:
            case None:
                return 0
            case Player.Me:
                return 1
            case Player.Enemy:
                return -1

    def determine_turn(self) -> Player:
        if self.last_turn is None:
            my_len = len(self.board.my_minions)
            enemy_len = len(self.board.enemy_minions)

            if my_len > enemy_len:
                return Player.Me
            elif my_len < enemy_len:
                return Player.Enemy
            else:
                return Player.Me if random.random() < 0.5 else Player.Enemy
        else:
            return ~self.last_turn

    def determine_attacker(self, minions: list[Minion]) -> Minion | None:
        return min(
            (m for m in minions if m.attack > 0),
            key=lambda m: m.attack_count,
            default=None,
        )

    def determine_target(self, minions: list[Minion]) -> Minion | None:
        if len(minions) == 0:
            return None

        taunt_minions = [m for m in minions if m.taunt]
        if len(taunt_minions) > 0:
            return random.choice(taunt_minions)

        non_stealth_minions = [m for m in minions if not m.stealth]
        if len(non_stealth_minions) > 0:
            return random.choice(non_stealth_minions)

        return random.choice(minions)

    def handle_event(self, event: event.Event) -> None:
        match event.type:
            case "pre_attack":
                pass
            case "post_attack":
                pass
            case "minion_died":
                for effect in event.minion.deathrattles:
                    effect.apply(self.board)
                for handler in self.board.event_handlers[event]:
                    handler.apply(self.board)
            case "minion_summoned":
                pass
            case "minion_buffed":
                pass
            case "deathrattle_triggered":
                pass
            case "battlecry_triggered":
                pass
            case "space_available":
                pass
            case "divine_shield_gained":
                pass
