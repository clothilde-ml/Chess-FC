from data_struct import Player, Pos

# ======================== Constantes de jeu ========================

PAWN_START_COL: dict[Player, int] = {Player.WHITE:  1, Player.BLACK:  7}
WHITE_GOAL_COLS: frozenset[int] = frozenset({7, 8})  # colonnes H et I
BLACK_GOAL_COLS: frozenset[int] = frozenset({0, 1})  # colonnes A et B

PAWN_FORWARD:   dict[Player, int] = {Player.WHITE:  1, Player.BLACK: -1}

ROOK_DIRS:   list[Pos] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
BISHOP_DIRS: list[Pos] = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
QUEEN_DIRS:  list[Pos] = ROOK_DIRS + BISHOP_DIRS

KNIGHT_JUMPS: list[Pos] = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
]