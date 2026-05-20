import chess.engine

engine = chess.engine.SimpleEngine.popen_uci(
    "./stockfish/stockfish-ubuntu-x86-64-avx2"
)

def analyze_position(board):

    result = engine.analyse(
        board,
        chess.engine.Limit(depth=12),
        multipv=3
    )

    move_lines = []

    best_eval = 0

    for line in result:

        score_obj = line["score"].white()

        if score_obj.is_mate():

            mate = score_obj.mate()

            if mate > 0:
                score = f"M{mate}"
            else:
                score = f"-M{abs(mate)}"

        else:

            score = score_obj.score()

            if score is None:
                score = 0

        if line.get("multipv") == 1:
            best_eval = score

        pv = line.get("pv")

        line_board = board.copy()

        formatted_line = ""

        if pv:

            for i, pv_move in enumerate(pv):

                san = line_board.san(pv_move)

                if line_board.turn == chess.WHITE:

                    formatted_line += (
                        f"{line_board.fullmove_number}. {san} "
                    )

                else:

                    if i == 0:

                        formatted_line += (
                            f"{line_board.fullmove_number}... {san} "
                        )

                    else:

                        formatted_line += f"{san} "

                line_board.push(pv_move)

        move_lines.append({
            "eval": score,
            "line": formatted_line.strip()
        })

    return {
        "best_eval": best_eval,
        "lines": move_lines
    }