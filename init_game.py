from data_struct import GameState, Player, Piece, PieceKind, Pos, empty_grid, grid_set

# ======================== État initial ========================

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
