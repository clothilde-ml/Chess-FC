from typing import NamedTuple, Optional
from enum import Enum

# ======================== Joueurs ========================

class Player(Enum):
    WHITE = 1
    BLACK = 2

def opponent(player: Player) -> Player:
    return Player.BLACK if player == Player.WHITE else Player.WHITE

# ======================== Types de pièces ========================

class PieceKind(Enum):
    PAWN   = "P"    # pion
    ROOK   = "R"    # tour
    BISHOP = "B"    # fou
    KNIGHT = "N"    # cavalier
    QUEEN  = "Q"    # reine (après promotion)

# ======================== Types de coup ========================

class MoveKind(Enum):
    NORMAL     = "normal"
    CAPTURE    = "capture"
    BALL_PASS  = "ball_pass"
    EN_PASSANT = "en_passant"
    PROMOTION  = "promotion"

# ======================== Structures de base ========================

Pos = tuple[int, int]  # (row, col)

class Piece(NamedTuple):
    kind:   PieceKind
    player: Player

class Move(NamedTuple):
    src:          Pos
    dst:          Pos
    kind:         MoveKind
    promotion_to: Optional[PieceKind] = None


# ======================== Plateau ========================

Grid = tuple[tuple[Optional[Piece], ...], ...]

BOARD_ROWS: int = 7
BOARD_COLS: int = 9

INVALID_POSITIONS: frozenset[Pos] = frozenset({
    (0, 0), (0, 1), (1, 0), (1, 1),  # coin bas-gauche
    (0, 7), (0, 8), (1, 7), (1, 8),  # coin bas-droite
    (5, 0), (5, 1), (6, 0), (6, 1),  # coin haut-gauche
    (5, 7), (5, 8), (6, 7), (6, 8),  # coin haut-droite
})

def is_valid_pos(pos: Pos) -> bool:
    """True si la position est dans les limites et hors des coins coupés."""
    row, col = pos
    return (
        0 <= row < BOARD_ROWS
        and 0 <= col < BOARD_COLS
        and pos not in INVALID_POSITIONS
    )

def grid_get(grid: Grid, pos: Pos) -> Optional[Piece]:
    row, col = pos
    return grid[row][col]

def grid_set(grid: Grid, pos: Pos, piece: Optional[Piece]) -> Grid:
    """Retourne une nouvelle grille avec la case pos mise à jour."""
    row, col = pos
    rows = [list(r) for r in grid]
    rows[row][col] = piece
    return tuple(tuple(r) for r in rows)

def empty_grid() -> Grid:
    """Retourne une grille vide"""
    return tuple(
        tuple(None for _ in range(BOARD_COLS))
        for _ in range(BOARD_ROWS)
    )
    
# ======================== Etat du jeu (hashable) ========================
    
class GameState(NamedTuple):
    grid:              Grid
    ball:              Pos
    current_player:    Player
    en_passant_target: Optional[Pos]