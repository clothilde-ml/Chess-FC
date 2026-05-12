from typing import Optional

from data_struct import Grid, Pos, Move, MoveKind
from data_struct import GameState, Player, opponent, Piece, PieceKind, Pos
from data_struct import empty_grid, grid_set, is_valid_pos, grid_get
from data_struct import move_piece, move_and_promote_piece, piece_prise
    
# ======================== Etat initial ========================

def initial_state() -> GameState:
    """
    Position de départ de Chess FC :
      WHITE : tour A3, fou A4, cavalier A5, pions B3 B4 B5
      BLACK : tour I5, fou I4, cavalier I3, pions H5 H4 H3
    Balle au centre : E4 = (row=3, col=4)
    """
    grid = empty_grid()
    setup: list[tuple[Pos, Piece]] = [
        ((2, 0), Piece(PieceKind.ROOK,   Player.WHITE)),  # A3
        ((3, 0), Piece(PieceKind.BISHOP, Player.WHITE)),  # A4
        ((4, 0), Piece(PieceKind.KNIGHT, Player.WHITE)),  # A5
        ((2, 1), Piece(PieceKind.PAWN,   Player.WHITE)),  # B3
        ((3, 1), Piece(PieceKind.PAWN,   Player.WHITE)),  # B4
        ((4, 1), Piece(PieceKind.PAWN,   Player.WHITE)),  # B5
        ((4, 8), Piece(PieceKind.ROOK,   Player.BLACK)),  # I5
        ((3, 8), Piece(PieceKind.BISHOP, Player.BLACK)),  # I4
        ((2, 8), Piece(PieceKind.KNIGHT, Player.BLACK)),  # I3
        ((4, 7), Piece(PieceKind.PAWN,   Player.BLACK)),  # H5
        ((3, 7), Piece(PieceKind.PAWN,   Player.BLACK)),  # H4
        ((2, 7), Piece(PieceKind.PAWN,   Player.BLACK)),  # H3
    ]
    for pos, piece in setup:
        grid = grid_set(grid, pos, piece)
    return GameState(
        grid=grid,
        ball=(3, 4),
        current_player=Player.WHITE,
        en_passant_target=None,
    )


# ======================== Déplacements par pièce ========================

PAWN_FORWARD:   dict[Player, int] = {Player.WHITE:  1, Player.BLACK: -1}

ROOK_DIRS:   list[Pos] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
BISHOP_DIRS: list[Pos] = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
QUEEN_DIRS:  list[Pos] = ROOK_DIRS + BISHOP_DIRS

KNIGHT_JUMPS: list[Pos] = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
]

# les pions peuvent avancer de deux cases depuis la colonne de départ
PAWN_START_COL: dict[Player, int] = {Player.WHITE:  1, Player.BLACK:  7}

WHITE_GOAL_COLS: frozenset[int] = frozenset({7, 8})  # colonnes H et I
BLACK_GOAL_COLS: frozenset[int] = frozenset({0, 1})  # colonnes A et B

def _knight_moves(grid: Grid, ball: Pos, src: Pos, player: Player) -> list[Move]:
    """Sauts en L du cavalier (8 destinations à checker). 
    Si sur la balle, génère des BALL_PASS."""
    moves: list[Move] = []
    on_ball = src == ball
    for d_row, d_col in KNIGHT_JUMPS:
        dst = (src[0] + d_row, src[1] + d_col)
        if not is_valid_pos(dst):
            continue
        if on_ball:
            moves.append(Move(src, dst, MoveKind.BALL_PASS))
        else:
            occupant = grid_get(grid, dst)
            if occupant is None:
                moves.append(Move(src, dst, MoveKind.NORMAL))
            elif occupant.player != player:
                moves.append(Move(src, dst, MoveKind.CAPTURE))
    return moves


def _sliding_moves(grid: Grid, ball: Pos, src: Pos, dirs: list[Pos], player: Player) -> list[Move]:
    """Mouvement sur toute les cases d'une direction pour toutes les directions (tour, fou, dame). 
    Si sur la balle, génère des BALL_PASS."""
    moves: list[Move] = []
    on_ball = src == ball
    for d_row, d_col in dirs:
        row, col = src
        while True: # on repète le dépalcement dans une direction jusqu'à être bloqué
            row += d_row
            col += d_col
            dst = (row, col)
            if not is_valid_pos(dst):
                break
            occupant = grid_get(grid, dst)
            if on_ball:
                moves.append(Move(src, dst, MoveKind.BALL_PASS))
                if occupant is not None:
                    break  # la balle s'arrête sur la première pièce
            else:
                if occupant is None:
                    moves.append(Move(src, dst, MoveKind.NORMAL))
                elif occupant.player != player:
                    moves.append(Move(src, dst, MoveKind.CAPTURE))
                    break
                else:
                    break  # bloqué par sa propre pièce 
    return moves

def apply_move(state: GameState, move: Move) -> GameState:
    """Applique un coup et retourne le nouvel état immuable."""
    grid = state.grid
    player = state.current_player
    new_ep: Optional[Pos] = None

    if move.kind == MoveKind.BALL_PASS:
        new_grid = grid
        new_ball = move.dst

    elif move.kind == MoveKind.EN_PASSANT:
        row_src, _ = move.src
        _, col_dst = move.dst
        new_grid = move_piece(grid, move.src, move.dst)
        new_grid = piece_prise(new_grid, (row_src, col_dst))
        new_ball = state.ball

    elif move.kind == MoveKind.PROMOTION:
        new_grid = move_and_promote_piece(grid, move.src, move.dst, Piece(PieceKind.QUEEN, player))
        new_ball = state.ball

    else:  # NORMAL ou CAPTURE
        new_grid = move_piece(grid, move.src, move.dst)
        new_ball = state.ball
        # Double pas (cible en passant = case intermédiaire)
        piece = grid_get(grid, move.src)
        if piece is not None and piece.kind == PieceKind.PAWN :
            row_src, col_src = move.src
            _, col_dst = move.dst
            if abs(col_dst - col_src) == 2:
                new_ep = (row_src, (col_src + col_dst) // 2)

    return GameState(
        grid=new_grid,
        ball=new_ball,
        current_player=opponent(player),
        en_passant_target=new_ep,
    )