<div align="center">

# Minimax Tic-Tac-Toe

*An unbeatable Tic-Tac-Toe AI built to study adversarial search*

[![Live Demo](https://img.shields.io/badge/play%20live-online-black?style=for-the-badge)](https://theemperorspath.github.io/tictactoe/)
[![Python](https://img.shields.io/badge/python-3.11+-black?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pygame](https://img.shields.io/badge/pygame-black?style=for-the-badge)](https://pygame.org)

</div>

---

The AI plays a perfect game of Tic-Tac-Toe using the minimax algorithm with alpha-beta pruning. It never loses - at best, you draw.

<br>

## How It Works

Minimax is a decision algorithm for two-player zero-sum games. It recursively simulates every possible future state from the current position and selects the move that maximises the AI's outcome, assuming the opponent always responds optimally.

Every terminal board state is assigned a utility score:

| Result | Score |
|--------|-------|
| X wins | `+1` |
| O wins | `-1` |
| Draw   | `0`  |

The maximising player (X) always picks the highest-scoring move; the minimising player (O) always picks the lowest. Both are assumed rational, so the algorithm evaluates the *guaranteed* outcome each side can force - not just what might happen.

<br>

## My Approach

I split the implementation across two files: `tictactoe.py` holds the game model and AI, and `main.py` drives the pygame interface.

I built the full game model first - `initial_state`, `player`, `actions`, `result`, `winner`, `terminal`, `utility` - before writing a single line of search. Having a clean, independently verifiable model made the recursive search much easier to reason about and debug.

For the search itself I wrote two mutually recursive functions rather than a single one:

```
minimax(board)
  |- max_value(board, alpha, beta)   <- X's turn: maximise score
  |- min_value(board, alpha, beta)   <- O's turn: minimise score
```

Keeping each player's perspective in its own function made the logic explicit and much easier to follow than the typical single-function approach with a `+1/-1` multiplier.

<br>

## Alpha-Beta Pruning

Naive minimax on an empty board visits up to **9! = 362,880 nodes**. Alpha-beta pruning eliminates branches that cannot possibly affect the final decision by maintaining two running bounds:

- **Alpha** - the best score the maximiser is guaranteed so far (a floor)
- **Beta** - the best score the minimiser is guaranteed so far (a ceiling)

When a node's value falls outside `[alpha, beta]`, the opponent already has a better option elsewhere and will never allow play to reach this branch - so the entire subtree is skipped.

```python
def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:   # minimiser won't allow this - prune
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:   # maximiser won't allow this - prune
            break
    return v
```

Both functions are called from `minimax()` with `alpha = -inf` and `beta = +inf`. As the search narrows in on the optimal line the window tightens, and increasingly large portions of the tree get pruned without ever being visited.

<br>

## Running Locally

```bash
pip install pygame
python runner.py
```

> `runner.py` is the plain pygame build. `main.py` is the web build target - it uses `asyncio` to yield to the browser event loop and won't run correctly with a standard Python interpreter.
