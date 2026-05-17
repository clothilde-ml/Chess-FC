import random
import ast
from typing import Callable

from data_struct import GameState, Player, Move
from game_rules import legals, is_final, score, apply_move, opponent

# Strategy : étant donné un état, retourne le coup choisi par le joueur courant
Strategy = Callable[[GameState], Move]

# ======================== Stratégies simples ========================

def strategy_random(state: GameState) -> Move:
    return random.choice(legals(state))


def strategy_first_legal(state: GameState) -> Move:
    return legals(state)[0]


# ======================== Min-Max ========================

def minmax(state: GameState) -> float:
    if is_final(state):
        return score(state)

    moves = legals(state)
    if state.current_player == Player.WHITE:
        return max(minmax(apply_move(state, m)) for m in moves)
    else:
        return min(minmax(apply_move(state, m)) for m in moves)


def minmax_action(state: GameState) -> tuple[float, Move | None]:
    if is_final(state):
        return score(state), None

    moves = legals(state)

    if state.current_player == Player.WHITE:
        best_score = float("-inf")
        best_move = None
        for m in moves:
            s, _ = minmax_action(apply_move(state, m))
            if s > best_score:
                best_score = s
                best_move = m
    else:
        best_score = float("+inf")
        best_move = None
        for m in moves:
            s, _ = minmax_action(apply_move(state, m))
            if s < best_score:
                best_score = s
                best_move = m

    return best_score, best_move


def strategy_minmax(state: GameState) -> Move:
    _, move = minmax_action(state)
    assert move is not None
    return move


def minmax_actions(state: GameState) -> tuple[float, list[Move]]:
    if is_final(state):
        return score(state), []

    moves = legals(state)
    results = [(minmax_actions(apply_move(state, m))[0], m) for m in moves]

    if state.current_player == Player.WHITE:
        best_score = max(s for s, _ in results)
    else:
        best_score = min(s for s, _ in results)

    best_moves = [m for s, m in results if s == best_score]
    return best_score, best_moves


def strategy_minmax_random(state: GameState) -> Move:
    _, moves = minmax_actions(state)
    return random.choice(moves)


# ======================== Élagage alpha-beta ========================

# WHITE : goal = colonnes 7-8, BLACK : goal = colonnes 0-1.
_BOARD_COLS = 9

def heuristic(state: GameState) -> float:
    _, col = state.ball
    return (col - (_BOARD_COLS - 1) / 2) / ((_BOARD_COLS - 1) / 2)


DEFAULT_DEPTH = 4


def alphabeta(
    state: GameState, depth: int = DEFAULT_DEPTH,
    alpha: float = float("-inf"), beta: float  = float("+inf"),
) -> float:
    if is_final(state):
        return score(state)
    if depth == 0:
        return heuristic(state)

    if state.current_player == Player.WHITE:
        value = float("-inf")
        for m in legals(state):
            value = max(value, alphabeta(apply_move(state, m), depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float("+inf")
        for m in legals(state):
            value = min(value, alphabeta(apply_move(state, m), depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def alphabeta_action(
    state: GameState, depth: int = DEFAULT_DEPTH,
    alpha: float = float("-inf"), beta: float  = float("+inf"),
) -> tuple[float, list[Move]]:
    if is_final(state):
        return score(state), []
    if depth == 0:
        return heuristic(state), []

    best_moves: list[Move] = []

    if state.current_player == Player.WHITE:
        best_score = float("-inf")
        for m in legals(state):
            s, _ = alphabeta_action(apply_move(state, m), depth - 1, alpha, beta)
            if s > best_score:
                best_score = s
                best_moves = [m]
            elif s == best_score:
                best_moves.append(m)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
    else:
        best_score = float("+inf")
        for m in legals(state):
            s, _ = alphabeta_action(apply_move(state, m), depth - 1, alpha, beta)
            if s < best_score:
                best_score = s
                best_moves = [m]
            elif s == best_score:
                best_moves.append(m)
            beta = min(beta, best_score)
            if alpha >= beta:
                break

    return best_score, best_moves


def strategy_alphabeta(state: GameState) -> Move:
    _, moves = alphabeta_action(state)
    return random.choice(moves)
