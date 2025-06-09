import random
from copy import deepcopy

from loguru import logger

from . import events
from .board import Board, Player
from .deathrattle import Deathrattle, SummonBeetle
from .minion import Minion

# random.seed(1337)

logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="{level.icon} | Turn: {extra[turn]!s} | {message}",
    level="INFO",
    filter=lambda record: record["extra"].setdefault("turn", "N/A"),
)


class Simulator:
    def __init__(self, my_minions: list[Minion], enemy_minions: list[Minion]):
        self.logger = logger.bind(turn=None)
        self.board = Board.from_minions(
            a=deepcopy(my_minions),
            b=deepcopy(enemy_minions),
        )
        self.last_turn: Player | None = None

    def perform_attack(
        self,
        attacking_player: Player,
        attacker: Minion,
        attacker_minions: list[Minion],
        target: Minion,
        target_minions: list[Minion],
    ) -> None:
        self.logger.info(f"{attacker} attacks {target}")

        self.handle_event(
            events.PreAttack(
                player=attacking_player,
                attacker_uuid=attacker.uuid,
                target_uuid=target.uuid,
            )
        )

        # do the trade
        attacker.health -= target.attack
        target.health -= attacker.attack
        attacker.attack_count += 1

        self.handle_event(
            events.PostAttack(
                player=attacking_player,
                attacker_uuid=attacker.uuid,
                target_uuid=target.uuid,
            )
        )

        # check if target dies
        if target.health <= 0:
            self.logger.info(f"{target} dies")
            index = target_minions.index(target)
            target_minions.remove(target)
            self.board.dead_minions[~attacking_player].add(target)
            self.handle_event(
                events.MinionDied(
                    player=~attacking_player,
                    minion_uuid=target.uuid,
                    minion_index=index,
                )
            )

        # check if attacker dies
        if attacker.health <= 0:
            self.logger.info(f"{attacker} dies")
            index = attacker_minions.index(attacker)
            attacker_minions.remove(attacker)
            self.board.dead_minions[attacking_player].add(attacker)
            self.handle_event(
                events.MinionDied(
                    player=attacking_player,
                    minion_uuid=attacker.uuid,
                    minion_index=index,
                )
            )

    def simulate(self) -> int:
        winner: Player | None = None

        while True:
            # 1. determine whose turn it is
            turn = self.determine_turn()
            self.logger = self.logger.bind(turn=turn)
            self.logger.info(f"Turn: {turn}")

            attacker_minions, target_minions = (
                (self.board.minions[Player.A], self.board.minions[Player.B])
                if turn == Player.A
                else (self.board.minions[Player.B], self.board.minions[Player.A])
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
                    self.logger.info(f"No target found - winner is {~turn}")
                    winner = ~turn
                    break

            # 4. perform the attack
            self.perform_attack(
                turn, attacker, attacker_minions, target, target_minions
            )

            # 5. update the board
            self.last_turn = turn

        match winner:
            case None:
                return 0
            case Player.A:
                return 1
            case Player.B:
                return -1

    def determine_turn(self) -> Player:
        if self.last_turn is None:
            my_len = len(self.board.minions[Player.A])
            enemy_len = len(self.board.minions[Player.B])

            if my_len > enemy_len:
                return Player.A
            elif my_len < enemy_len:
                return Player.B
            else:
                return Player.A if random.random() < 0.5 else Player.B
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

    def handle_event(self, event: events.Event) -> None:
        match event.type:
            case "minion_summoned":
                self.logger.info(f"{event.minion_uuid} summoned")
            case "minion_died":
                minion = next(
                    m
                    for m in self.board.dead_minions[event.player]
                    if m.uuid == event.minion_uuid
                )
                if minion.name == "Buzzing Vermin":
                    for deathrattle in minion.deathrattles:
                        self.handle_deathrattle(event, deathrattle)

    def handle_deathrattle(
        self, event: events.MinionDied, deathrattle: Deathrattle
    ) -> None:
        player = event.player
        match deathrattle.type:
            case "summon_beetle":
                if not self.board.has_space(player):
                    return

                attack, health = self.board.metadata[player].beetles
                beetle = Minion.custom("Beetle", attack=attack, health=health)
                minion_index = len(self.board.minions[player])
                self.board.minions[player].insert(minion_index, beetle)
                self.handle_event(
                    events.MinionSummoned(
                        player=player,
                        minion_uuid=beetle.uuid,
                        minion_index=minion_index,
                    )
                )

            case "summon_cublings":
                cubs = [Minion.custom("Cubling", attack=0, health=0) for _ in range(2)]
                for cub in cubs:
                    if not self.board.has_space(player):
                        continue

                    minion_index = len(self.board.minions[player])
                    self.board.minions[player].insert(minion_index, cub)
                    self.handle_event(
                        events.MinionSummoned(
                            player=player,
                            minion_uuid=cub.uuid,
                            minion_index=minion_index,
                        )
                    )

        self.handle_event(
            events.DeathrattleTriggered(
                minion_uuid=event.minion_uuid,
            )
        )
