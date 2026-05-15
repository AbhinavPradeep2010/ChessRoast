import chess
import chess.pgn
import chess.engine
import io

pgn_text = """
[Event "?"]
[Site "?"]
[Date "2026.05.11"]
[Round "?"]
[White "Player1"]
[Black "Player2"]
[Result "*"]

1. e4 e5 2. Nf3 Nc6 3. Bc4 Nd4??
"""



pgn = chess.pgn.read_game(io.StringIO(pgn_text))

board = pgn.board()

engine = chess.engine.SimpleEngine.popen_uci(
    "../stockfish/stockfish-ubuntu-x86-64-avx2"
)

for move in pgn.mainline_moves():
    print("Move:", move)

    board.push(move)

    result = engine.analyse(board, chess.engine.Limit(depth=12))

    print("Evaluation:", result["score"])

engine.quit()