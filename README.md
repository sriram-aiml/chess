# ♟️ LLM vs LLM Chess

Two AI models play chess against each other — GPT-4.1-mini (White) vs Claude Sonnet (Black) — with `python-chess` enforcing legal moves.

## Why?

LLMs understand chess *concepts* but can't reliably track board state. Early experiments showed models making illegal moves, placing pieces on wrong squares, and corrupting board representations. This project solves that with a hybrid approach: LLMs pick moves, `python-chess` validates them.

## How It Works

```
┌─────────────┐    board state    ┌──────────────┐
│  GPT-4.1    │ ◄──────────────── │              │
│  (White)    │ ────── move ────► │ python-chess │
└─────────────┘                   │  (validator) │
                                  │              │
┌─────────────┐    board state    │              │
│   Claude    │ ◄──────────────── │              │
│  (Black)    │ ────── move ────► │              │
└─────────────┘                   └──────────────┘
```

1. The board state is sent to the active player (as text)
2. The LLM responds with a move in Standard Algebraic Notation (e.g. `e4`, `Nf3`)
3. `python-chess` validates the move — illegal moves trigger a retry (up to 3 attempts)
4. The updated board is sent to the opponent
5. Repeat until checkmate, stalemate, or draw

## Key Learnings

- **LLMs can't do spatial reasoning** — they pattern-match chess language but fail at 2D coordinate mapping
- **Board format matters** — asking LLMs to output a full 2D Python list is error-prone; SAN notation is far more reliable
- **Validation is essential** — without `python-chess`, games devolve into illegal moves within 5-10 turns
- **Stronger models play better** — Claude Sonnet made fewer errors than Haiku, but none match a real chess engine

## Setup

```bash
pip install python-chess litellm
```

Set your API keys:
```bash
export OPENAI_API_KEY=your-key
export ANTHROPIC_API_KEY=your-key
```

## Run

```bash
python chess_llm_battle.py
```

## Models Tested

| Model | Role | Notes |
|-------|------|-------|
| GPT-4.1-mini | White | Decent opening play, occasional mid-game errors |
| Claude 3.5 Haiku | Black | Fast but weak spatial reasoning |
| Claude Sonnet 4 | Black | Significantly better board awareness |

## Tech Stack

- **LiteLLM** — unified API for calling OpenAI + Anthropic models
- **python-chess** — move validation, board state management, game-over detection
- **Python 3.10+**

## License

MIT
