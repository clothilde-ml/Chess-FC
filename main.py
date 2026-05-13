from data_struct import GameState, Piece, PieceKind, Player, grid_get, is_valid_pos, piece_prise
from game_rules import ROOK_DIRS, BISHOP_DIRS, KNIGHT_JUMPS
from game_rules import initial_state, _sliding_moves, _knight_moves, _pawn_moves, apply_move
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
    
    SEP = "=" * 10
    
    knight_moves = _knight_moves(state.grid, state.ball, (3,0), state.current_player) 
    print(SEP, f"Mouvements du cavalier blanc ({len(knight_moves)}) :", SEP, "\n")
    for m in knight_moves :
        new_state = apply_move(state, m)
        pprint(new_state)
    
    pawn_moves = _pawn_moves(state.grid, state.ball, None, (3,1), state.current_player) 
    print(SEP, f"Mouvements du pion blanc B4 ({len(pawn_moves)}) :", SEP, "\n")
    for m in pawn_moves :
        new_state = apply_move(state, m)
        pprint(new_state)
        
    state_rook = GameState(
        grid=piece_prise(state.grid, (2,1)), # retirer le pion pour tester les coups
        ball=state.ball,
        current_player=state.current_player,
        en_passant_target=state.en_passant_target,
    )
    rook_moves = _sliding_moves(state_rook.grid, state_rook.ball, (2,0), ROOK_DIRS, state_rook.current_player) 
    print(SEP, f"Mouvements de la tour blanche ({len(rook_moves)}) :", SEP, "\n")
    for m in rook_moves :
        new_state = apply_move(state_rook, m)
        pprint(new_state)
    
    state_bishop = GameState(
        grid=piece_prise(state.grid, (3,1)), # retirer le pion pour tester les coups
        ball=state.ball,
        current_player=state.current_player,
        en_passant_target=state.en_passant_target,
    )
    bishop_moves = _sliding_moves(state_bishop.grid, state_bishop.ball, (4,0), BISHOP_DIRS, state_bishop.current_player) 
    print(SEP, f"Mouvements du fou blanc ({len(bishop_moves)}) :", SEP, "\n")
    for m in bishop_moves :
        new_state = apply_move(state_bishop, m)
        pprint(new_state)
    
if __name__ == "__main__":
    main()