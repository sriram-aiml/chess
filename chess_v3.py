
from litellm import completion
import time
gpt_model = "o4-mini"
#claude_model = "claude-opus-4-20250514"
claude_model = "o4-mini"

import chess
board = chess.Board()

import chess.svg
from IPython.display import display, SVG

gpt_system = """You are a world-class chess player named PLAYER_GPT playing White.
You will receive the current board state and a list of legal moves.
Respond with ONLY your next move in Standard Algebraic Notation (SAN).

Output ONLY the move. No explanation, no board, no commentary.
Example valid output: e4
Example valid output: Nf3"""

claude_system = """You are a world-class chess player named PLAYER_CLAUDE playing Black.
You will receive the current board state and a list of legal moves.
Respond with ONLY your next move in Standard Algebraic Notation (SAN).

Output ONLY the move. No explanation, no board, no commentary.
Example valid output: e5
Example valid output: Nf6"""

def call_gpt(gpt_system):
    legal_moves = [board.san(m) for m in board.legal_moves]
    user_msg = f"Current board:\n{str(board)}\n\nYour legal moves: {', '.join(legal_moves)}\n\nPick the best move."
    messages = [
        {"role": "system", "content": gpt_system},
        {"role": "user", "content": user_msg}
    ]
    for attempt in range(10):
        response = completion(model=gpt_model, messages=messages)
        move = response.choices[0].message.content.strip().split('\n')[0].split()[0]
        try:
            board.push_san(move)
            print(f"GPT plays: {move}")
            display(SVG(chess.svg.board(board, lastmove=board.peek(), size=400)))
            return not board.is_game_over()
        except Exception as e:
            print(f"GPT invalid move '{move}' (attempt {attempt+1}): {e}")
            messages.append({"role": "assistant", "content": move})
            messages.append({"role": "user", "content": f"'{move}' is illegal. Pick from: {', '.join(legal_moves)}"})
    print("GPT failed 10 attempts, ending game.")
    return False

def call_claude(claude_system):
    legal_moves = [board.san(m) for m in board.legal_moves]
    user_msg = f"Current board:\n{str(board)}\n\nYour legal moves: {', '.join(legal_moves)}\n\nPick the best move."
    messages = [
        {"role": "system", "content": claude_system},
        {"role": "user", "content": user_msg}
    ]
    for attempt in range(10):
        response = completion(model=claude_model, messages=messages)
        move = response.choices[0].message.content.strip().split('\n')[0].split()[0]
        try:
            board.push_san(move)
            print(f"Claude plays: {move}")
            display(SVG(chess.svg.board(board, lastmove=board.peek(), size=400)))
            return not board.is_game_over()
        except Exception as e:
            print(f"Claude invalid move '{move}' (attempt {attempt+1}): {e}")
            messages.append({"role": "assistant", "content": move})
            messages.append({"role": "user", "content": f"'{move}' is illegal. Pick from: {', '.join(legal_moves)}"})
    print("Claude failed 10 attempts, ending game.")
    return False

while True:
    if not call_gpt(gpt_system):
        break
    time.sleep(5)
    if not call_claude(claude_system):
        break
    time.sleep(5)