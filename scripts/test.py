import chess
import chess.engine

board = chess.Board()

engine = chess.engine.SimpleEngine.popen_uci(
    "../stockfish/stockfish-ubuntu-x86-64-avx2"
)

result = engine.analyse(board, chess.engine.Limit(depth=15))

print(result["score"])

engine.quit()