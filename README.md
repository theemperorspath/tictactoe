# Minimax Tic-Tac-Toe

**Play it live → [theemperorspath.github.io/tictactoe](https://theemperorspath.github.io/tictactoe/)**

My AI in Python project implementing an unbeatable Tic-Tac-Toe opponent using the minimax algorithm with alpha-beta pruning. The AI never loses - at best, you draw.

---

## The Algorithm

Minimax is a decision-making algorithm for two-player zero-sum games. It works by exhaustively simulating every possible game state from the current position and choosing the move that maximises the AI's outcome while assuming the opponent always plays optimally.

Each board state is assigned a score:
- **+1** - X wins
- **-1** - O wins
- **0** - draw

The maximising player (X) always picks the move with the highest score; the minimising player (O) always picks the move with the lowest. Both players are assumed to be rational, so the algorithm evaluates the *best* outcome each side can force - not just what might happen.

---

## My Approach

The core logic lives in `tictactoe.py`. I implemented the full game model first - `initial_state`, `player`, `actions`, `result`, `winner`, `terminal`, and `utility` - before touching the search. Having a clean model made the recursive search straightforward to reason about.

For the search itself I wrote two mutually recursive functions, `max_value` and `min_value`, rather than a single `minimax` function. This made the logic for each player explicit and easier to follow. `minimax` then just calls whichever side is to move and tracks the best action found.

---

## Alpha-Beta Pruning

The naive minimax explores every reachable game state, which on an empty board means 9! = 362,880 nodes. Alpha-beta pruning cuts this down significantly by tracking two bounds as the search runs:

- **Alpha** - the best score the maximiser is *guaranteed* so far (a floor)
- **Beta** - the best score the minimiser is *guaranteed* so far (a ceiling)

When a node's value falls outside the `[alpha, beta]` window, we know the opponent will never let play reach this state - they already have a better option - so the entire subtree is pruned.

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

Alpha starts at −∞ and beta starts at +∞. As the search narrows in on the optimal line, these bounds tighten and prune away irrelevant branches - the AI never wastes time evaluating moves that can't possibly influence the final decision.

---

## Running Locally

```bash
pip install pygame
python runner.py
```

`runner.py` is the plain pygame version. `main.py` is the pygbag build target (used for the web deployment) and uses `asyncio` to yield to the browser event loop - don't run it directly with a standard Python interpreter.
