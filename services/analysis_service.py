import chess
import chess.pgn
import io

from services.engine_service import analyze_position
from services.opening_service import is_book_move, get_opening_name
from utils.classifier import classify_move


def analyze_game(pgn_text):
    moves = []
    evals = []
    all_lines = []
    san_moves = []
    move_data = []
    fen = "start"
    opening_name = None

    pgn = chess.pgn.read_game(io.StringIO(pgn_text))

    board = pgn.board()

    for move in pgn.mainline_moves():
        move_lines = []

        current_san = board.san(move)

        book, _ = is_book_move(
            moves,
            current_san
        )

        moves.append(move.uci())

        opening = get_opening_name(moves)

        if opening:
            opening_name = opening
        san_moves.append(current_san)

        turn = "white" if board.turn == chess.WHITE else "black"

        board.push(move)

        analysis_result = analyze_position(board)

        best_eval = analysis_result["best_eval"]

        move_lines = analysis_result["lines"]

        evals.append(best_eval)

        if len(evals) > 1:

            previous_eval = evals[-2]
            current_eval = evals[-1]

            classification_data = classify_move(previous_eval, current_eval, turn, book)

            classification = "book" if book else classification_data['classification']

            move_data.append({
                "move_number": len(san_moves),
                "move": san_moves[-1],
                "classification": classification,
                "swing": classification_data['probability_swing'],
                "opening": opening_name,
            })

        else:

            move_data.append({
                "move_number": 1,
                "move": san_moves[-1],
                "classification": "book",
                "swing": 0,
                "opening": opening_name,
            })

        all_lines.append(move_lines)

        fen = board.fen()


    return {
        "fen": board.fen(),
        "moves": moves,
        "evals": evals,
        "all_lines": all_lines,
        "san_moves": san_moves,
        "move_data": move_data,
        "opening_name": opening_name,
    }
