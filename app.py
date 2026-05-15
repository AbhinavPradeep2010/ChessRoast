from flask import Flask, render_template, request
import requests
import json
import chess
import chess.pgn
import chess.engine
import io



app = Flask(__name__)

engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-ubuntu-x86-64-avx2")


@app.route("/", methods=["GET", "POST"])
def home():

    analysis = []
    moves = []
    evals = []
    all_lines = []
    san_moves = []
    
    fen = "start"

    if request.method == "POST":
        
        pgn_text = request.form["pgn"]

        pgn = chess.pgn.read_game(io.StringIO(pgn_text))

        board = pgn.board()

        for move in pgn.mainline_moves():
            move_lines = []

            moves.append(move.uci())

            san_moves.append(board.san(move))

            board.push(move)

            result = engine.analyse(
                board,
                chess.engine.Limit(depth=12),
                multipv=5
            )

            best_eval = 0

            for line in result:

                score = line["score"].white().score()

                if score is None:
                    score = 0

                if line["multipv"] == 1:
                    best_eval = score

                pv = line.get("pv")

                line_board = board.copy()

                pv_san = []

                formatted_line = ""

                if pv:

                    move_number = line_board.fullmove_number

                    is_white = line_board.turn == chess.WHITE

                    for i, pv_move in enumerate(pv[:10]):

                        san = line_board.san(pv_move)

                        if line_board.turn == chess.WHITE:

                            formatted_line += f"{line_board.fullmove_number}. {san} "

                        else:

                            if i == 0:
                                formatted_line += f"{line_board.fullmove_number}... {san} "
                            else:
                                formatted_line += f"{san} "

                        line_board.push(pv_move)

                move_lines.append({
                    "eval": round(score / 100, 1),
                    "line": formatted_line.strip()
                })

            evals.append(best_eval)

            all_lines.append(move_lines)

            fen = board.fen()


    return render_template("index.html", analysis = analysis, fen = fen, moves = moves, evals = evals, all_lines=all_lines, san_moves=san_moves)


if __name__ == "__main__":  
    app.run(debug=False)
