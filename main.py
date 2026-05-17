import time

from data_struct import GameState, Piece, PieceKind, Player, grid_get, is_valid_pos, piece_prise
from game_rules import ROOK_DIRS, BISHOP_DIRS
from game_rules import initial_state, _sliding_moves, _knight_moves, _pawn_moves, legals
from game_rules import apply_move, is_goal, is_final, score, opponent
from interface import pprint, move_to_str
from strategies import (
    Strategy,
    strategy_random, strategy_first_legal,
    strategy_minmax, strategy_minmax_random,
    strategy_alphabeta,
)

def play_game(strategy_white: Strategy, strategy_black: Strategy, debug: bool = False) -> float:
    """Boucle de jeu : alterne WHITE/BLACK jusqu'à état final, retourne le score."""
    state = initial_state()
    strategies = {Player.WHITE: strategy_white, Player.BLACK: strategy_black}
    i = 0
    while not is_final(state):
        if debug:
            pprint(state)
        move = strategies[state.current_player](state)
        if debug:
            piece = grid_get(state.grid, move.src)
            if piece is not None:
                print(" ->", move_to_str(move, piece))
        state = apply_move(state, move)
        time.sleep(0.2)
        i += 1
        if i % 10 == 0:
            if not debug:
                pprint(state)
            input(f"--- Tour {i} ---")
    if debug:
        pprint(state)
        print("Score final :", score(state))
    return score(state)


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
        piece = grid_get(state.grid, m.src)
        assert piece != None
        print(" ", move_to_str(m, piece))
        new_state = apply_move(state, m)
        pprint(new_state)
    
    pawn_moves = _pawn_moves(state.grid, state.ball, None, (3,1), state.current_player) 
    print(SEP, f"Mouvements du pion blanc B4 ({len(pawn_moves)}) :", SEP, "\n")
    for m in pawn_moves :
        piece = grid_get(state.grid, m.src)
        assert piece != None
        print(" ", move_to_str(m, piece))
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
        piece = grid_get(state.grid, m.src)
        assert piece != None
        print(" ", move_to_str(m, piece))
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
        piece = grid_get(state.grid, m.src)
        assert piece != None
        print(" ", move_to_str(m, piece))
        new_state = apply_move(state_bishop, m)
        pprint(new_state)
        
    SEP2 = "=" * 60
    print(SEP2)
    print(" "*20, "ALL LEGAL MOVES")
    print(SEP2)
    
    moves = legals(state)
    print(f"Coups légaux WHITE au départ : {len(moves)}")
    for m in sorted(moves):
        piece = grid_get(state.grid, m.src)
        assert piece != None
        print(" ", move_to_str(m, piece))
    
    assert not is_final(state)
    assert score(state) == 0
    assert not is_goal(state.ball, state.current_player)
    assert not is_goal(state.ball, opponent(state.current_player))

    print(SEP2)
    print(" " * 18, "TEST DES STRATÉGIES")
    print(SEP2)
    
    print("\n--- alphabeta (WHITE) vs random (BLACK) ---")
    s = play_game(strategy_alphabeta, strategy_random, debug=True)
    print("Résultat :", s)

    print("\n--- random vs random ---")
    s = play_game(strategy_random, strategy_random, debug=True)
    print("Résultat :", s)

    print("\n--- first_legal vs random ---")
    s = play_game(strategy_first_legal, strategy_random, debug=False)
    print("Résultat :", s)

    

if __name__ == "__main__":
    main()