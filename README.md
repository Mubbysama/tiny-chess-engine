# Tiny Chess Engine

A complete chess engine in one compact Python file (`engine.py`, about 10 KB of
source, standard library only). It plays legal chess through a search, not a
book of moves: alpha-beta search with quiescence, a transposition table with
Zobrist hashing, killer moves, history heuristic, MVV-LVA move ordering,
null-move pruning, late-move reductions, check extensions, futility pruning,
and a piece-square evaluation with pawn structure (doubled, isolated and
passed pawns, bishop pair) and tapered king tables. The board uses the 0x88
representation. The search runs to a fixed budget of 100,000 nodes per move,
so it is deterministic: same position, same move, every time.

## What it does

Given a position, the engine lists every legal move (including castling,
en passant and promotions), searches them, and returns the best one in UCI
notation (for example `e2e4`). It was built to play full games against the
house gauntlet in the make.fun tiny-chess bounty, where the whole program had
to fit in 4,096 bytes: the submitted entry was this same source packed into a
4 KB file, so the engine is written compactly, with short names and no
comments. This repository holds the readable source.

## How to run it

Python 3, standard library only, nothing to install.

Play a game against the make.fun tiny-chess game server (the server the
bounty used), with its URL in `MAKEFUN_ENV_URL`:

```sh
MAKEFUN_ENV_URL=http://localhost:8080 python3 engine.py
```

The engine polls the server for its turn and posts its move back.

Or use the search directly in your own code:

```python
from engine import fen, gen, root, m2u, SF

fen(SF)                            # load the start position
moves = [m2u(m) for m in gen()]    # all legal moves, in UCI notation
best = root(moves)                 # search and pick the best move
print(m2u(best))
```

## What it achieved

Entered in the make.fun tiny-chess-01 bounty. The official dev grade scored
it at **1,451 Elo**, clearing the 1,154 practice floor by 297 points, which
put the entry into the final. Local trials against the house gauntlet averaged
1,514 Elo over three trials (1,451 / 1,545 / 1,545), about 149 points above
the sunfish baseline of roughly 1,365. Perft tests passed on all six standard
positions, and the packed entry played 18 full trial games with no illegal
move, crash or time loss.

## License

MIT. See `LICENSE`.
