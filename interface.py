from data_struct import GameState, PieceKind, Player, Move, BOARD_COLS, BOARD_ROWS, grid_get, is_valid_pos

# ======================== Affichage d'un GameState ========================

def pprint(state: GameState) -> None:
    """Affiche l'état du jeu (ligne 7 en haut, colonne A à gauche)."""
    col_names = "ABCDEFGHI"
    ball_str = f"{col_names[state.ball[1]]}{state.ball[0] + 1}"
    ep_str = ""
    if state.en_passant_target is not None:
        r, c = state.en_passant_target
        ep_str = f"  en passant: {col_names[c]}{r + 1}"
    print(f" - Tour: {state.current_player.name}  Balle: {ball_str}{ep_str}\n")
    print("       A   B   C   D   E   F   G   H   I")
    print(" "*3, "-"*40)
    sym = {PieceKind.PAWN: "P", PieceKind.ROOK: "R", PieceKind.BISHOP: "B",
           PieceKind.KNIGHT: "N", PieceKind.QUEEN: "Q"}
    for row in range(BOARD_ROWS):
        cells = []
        for col in range(BOARD_COLS):
            pos = (row, col)
            if not is_valid_pos(pos):
                cells.append("    ")
                continue
            piece = grid_get(state.grid, pos)
            marker = "*" if pos == state.ball else " "
            if piece is None:
                cells.append(f"  {marker}.")
            else:
                color = "W" if piece.player == Player.WHITE else "B"
                cells.append(f" {marker}{color}{sym[piece.kind]}")
        print(f"{row + 1} | {''.join(cells)}   |")
    print(" "*3, "-"*40)
    print()

def move_to_str(move: Move) -> str:
    """Transforme (src: Pos, dst: Pos, kind: MoveKind, promotion_to: Optional[PieceKind])
        -> 'MoveKind (C4->C5)' ou 'promotion (C4->C5) [Q]"""
    cols = "ABCDEFGHI"
    src = f"{cols[move.src[1]]}{move.src[0] + 1}"
    dst = f"{cols[move.dst[1]]}{move.dst[0] + 1}"
    promo = f"={move.promotion_to.value}" if move.promotion_to else ""
    return f"{move.kind.value}({src}->{dst}) [{promo}]"