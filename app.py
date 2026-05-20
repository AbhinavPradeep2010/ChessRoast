from flask import Flask, render_template, request
import requests
import json
import chess
import chess.pgn
import io
import math
import os 
from roaster.classifier import classify_move
from services.engine_service import analyze_position



app = Flask(__name__)

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
