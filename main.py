from data_struct import GameState, Piece, PieceKind, Player, grid_get, is_valid_pos, piece_prise
from game_rules import ROOK_DIRS, BISHOP_DIRS, KNIGHT_JUMPS
from game_rules import initial_state, _sliding_moves, _knight_moves, apply_move
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
    
    knight_moves = _knight_moves(state.grid, state.ball, (3,0), state.current_player) 
    print(f"Mouvements du cavalier blanc ({len(knight_moves)}) :")
    for m in knight_moves :
        new_state = apply_move(state, m)
        pprint(new_state)
        
        
    state = GameState(
        grid=piece_prise(state.grid, (2,1)), # retirer le pion pour tester les coups
        ball=state.ball,
        current_player=state.current_player,
        en_passant_target=state.en_passant_target,
    )
    rook_moves = _sliding_moves(state.grid, state.ball, (2,0), ROOK_DIRS, state.current_player) 
    print(f"Mouvements de la tour blanche ({len(rook_moves)}) :")
    for m in rook_moves :
        new_state = apply_move(state, m)
        pprint(new_state)
    
if __name__ == "__main__":
    main()