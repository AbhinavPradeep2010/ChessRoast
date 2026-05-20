from flask import Flask, render_template, request
from services.analysis_service import analyze_game

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        pgn_text = request.form["pgn"]

        analysis_data = analyze_game(pgn_text)

        return render_template(
            "index.html",
            **analysis_data
        )

    return render_template(
        "index.html",
        fen="start",
        moves=[],
        evals=[],
        all_lines=[],
        san_moves=[],
        move_data=[],
        opening_name=None
    )


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":  
    app.run(debug=False)
