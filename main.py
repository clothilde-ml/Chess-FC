from data_struct import Piece, PieceKind, Player, grid_get, is_valid_pos
from game_rules import initial_state
from interface import pprint

def main() -> None:
    state = initial_state()
    pprint(state)

    assert is_valid_pos((3, 4))
    assert not is_valid_pos((0, 0))
    assert not is_valid_pos((6, 8))

    assert grid_get(state.grid, (2, 0)) == Piece(PieceKind.ROOK,   Player.WHITE)
    assert grid_get(state.grid, (4, 8)) == Piece(PieceKind.ROOK,   Player.BLACK)
    assert grid_get(state.grid, (3, 4)) is None
    assert state.ball == (3, 4)
    
if __name__ == "__main__":
    main()