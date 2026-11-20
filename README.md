# Tiny Chess Engine

A 4 KB chess engine for the make.fun tiny-chess-01 competition.
One file (`main.py`, 4096 bytes max), Python 3.13 standard library only,
deterministic, fixed node budget, no model calls.

## Board

10x12 mailbox. Squares 21..98, pieces 1 P, 2 N, 3 B, 4 R, 5 Q, 6 K
(white positive, black negative). Incremental state: pawn bitboards
(WP/BP), bishop counts (BC), king squares (KP), Zobrist hash (Z) with an
O(1) repetition counter, and tapered eval accumulators (A/D/Y).

## Evaluation

Tapered PeSTO (separate MG/EG tables for all six pieces, symmetric //16
quantization). Tiered passed-pawn bonus by rank (EG, half in MG), halved
when the square ahead is blocked. Bishop pair +35 MG / +50 EG.
Dynamic contempt -40. Adjudication magnet past ply 150.

## Search

PVS with null-window re-search, transposition table kept across moves
(cleared past 250k entries, mate-distance normalized, repetition scores
never stored), guarded null-move pruning, LMR, check extension, reverse
futility (85*d) and futility (120*d, promotions exempt), two killers per
ply, history heuristic, quiescence with delta pruning. Node limit 180000
per move, iterative deepening at the root, previous best move first.

## Results

Local practice trials: 2112 Elo (6-0-0) on trial-0/1/2, gauntlet 8/12
vs nodes-1M/2M. The entrypoint is packed from `clean_engine.py` with
the kit's own `node cli/makefun.mjs compress`; the readable source is
bundled beside the session for the transcript check.

## License

MIT. See LICENSE.
