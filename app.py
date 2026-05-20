from flask import Flask, render_template, request
import requests
import json
import chess
import chess.pgn
import chess.engine
import io
import math
import os 
from roaster.classifier import classify_move



app = Flask(__name__)

engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-ubuntu-x86-64-avx2")

TOKEN = os.getenv("LICHESS_TOKEN")


def is_book_move(move_list, played_move):
    try:
        response = requests.get(
            "https://explorer.lichess.ovh/masters",
            params={
                "play": ",".join(move_list)
            },
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "User-Agent": "ChessRoast/1.0"
            },
            timeout=5
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            return False, None

        data = response.json()

        for move_data in data.get("moves", []):

            if move_data["san"] == played_move:

                opening_data = data.get("opening")

                opening = None

                if opening_data:
                    opening = opening_data.get("name")

                return True, opening

        return False, None

    except Exception as e:

        print("Error occurred:", e)

        return False, None
    

def get_opening_name(move_list):

    try:

        response = requests.get(
            "https://explorer.lichess.ovh/masters",
            params={
                "play": ",".join(move_list)
            },
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "User-Agent": "ChessRoast/1.0"
            },
            timeout=5
        )

        if response.status_code != 200:
            return None

        data = response.json()

        opening_data = data.get("opening")

        if opening_data:
            return opening_data.get("name")

        return None

    except Exception as e:

        print("Opening lookup error:", e)

        return None


@app.route("/", methods=["GET", "POST"])
def home():

    moves = []
    evals = []
    all_lines = []
    san_moves = []
    move_data = []
    fen = "start"
    opening_name = None

    if request.method == "POST":
        
        pgn_text = request.form["pgn"]

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

            result = engine.analyse(
                board,
                chess.engine.Limit(depth=12),
                multipv=3
            )

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

                pv_san = []

                formatted_line = ""

                if pv:

                    move_number = line_board.fullmove_number

                    is_white = line_board.turn == chess.WHITE

                    for i, pv_move in enumerate(pv):

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
                    "eval": score,
                    "line": formatted_line.strip()
                })

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


    return render_template(
        "index.html",
        fen = fen,
        moves = moves,
        evals = evals,
        all_lines=all_lines,
        san_moves=san_moves,
        move_data=move_data,
        opening_name=opening_name,
)


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":  
    app.run(debug=False)
