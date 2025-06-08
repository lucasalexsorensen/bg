import random
from copy import deepcopy

from loguru import logger

from .board import Board, Player
from .minion import Minion

logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="{level.icon} {time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | Turn: {extra[turn]!s} | {message}",
    level="INFO",
    filter=lambda record: record["extra"].setdefault("turn", "N/A"),
)


def simulate_combat(my_minions: list[Minion], enemy_minions: list[Minion]) -> int:
    log = logger.bind(turn=None)
    board = Board(deepcopy(my_minions), deepcopy(enemy_minions))
    winner: Player | None = None

    while True:
        # 1. determine whose turn it is
        turn = determine_turn(board)
        log = log.bind(turn=turn)

        attacker_minions, target_minions = (
            (board.my_minions, board.enemy_minions)
            if turn == Player.ME
            else (board.enemy_minions, board.my_minions)
        )

        # 2. determine which minion will be attacking
        attacker = determine_attacker(attacker_minions)

        # 3. determine which minion will be targeted
        target = determine_target(target_minions)

        match (attacker, target):
            case (None, None):
                log.info("No attacker or target found - draw")
                winner = None
                break
            case (None, _):
                log.info("No attacker found - target wins")
                winner = turn
                break
            case (_, None):
                log.info("No target found - attacker wins")
                winner = ~turn
                break

        # 4. determine the outcome of the trade
        logger.info(
            f"{attacker} attacks {target}",
            turn=turn,
        )
        attacker.health -= target.attack
        target.health -= attacker.attack
        if attacker.health <= 0:
            attacker_minions.remove(attacker)
        if target.health <= 0:
            target_minions.remove(target)

    match winner:
        case None:
            return 0
        case Player.ME:
            return 1
        case Player.ENEMY:
            return -1


def determine_turn(board: Board) -> Player:
    if board.last_turn is None:
        return determine_first_turn(board)
    else:
        return ~board.last_turn


def determine_first_turn(board: Board) -> Player:
    my_len = len(board.my_minions)
    enemy_len = len(board.enemy_minions)

    if my_len > enemy_len:
        return Player.ME
    elif my_len < enemy_len:
        return Player.ENEMY
    else:
        return Player.ME if random.random() < 0.5 else Player.ENEMY


def determine_attacker(minions: list[Minion]) -> Minion | None:
    # from left-to-right, find the minion with the least attack count
    return min(
        (m for m in minions if m.attack > 0),
        key=lambda m: m.attack_count,
        default=None,
    )


def determine_target(minions: list[Minion]) -> Minion | None:
    if len(minions) == 0:
        return None

    taunt_minions = [m for m in minions if m.taunt]
    if len(taunt_minions) > 0:
        return random.choice(taunt_minions)

    return random.choice(minions)
