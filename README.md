# Tiny Chess — Fresh Engine

A compact chess engine for the make.fun tiny-chess-01 competition.
Single-file engine in `main.py` (LZMA-packed, ≤4096 bytes), Python 3.13
standard library only, deterministic, no model calls.

## Design

- Mailbox 10x12 board, tapered PeSTO evaluation (asymmetric, //16
  round-to-nearest quantized, MG and EG fully separate tables).
- Bitboard pawn tracking (WP/BP) + incremental bishop counts; ev()
  iterates only active pawn bits, no 78-square loop.
- Iterative deepening + PVS + transposition table (mate-normalized,
  kept between moves, cleared only if >250000 entries).
- Null-move pruning (non-PV only), LMR, check extension.
- 2 killers per ply (with guard) + history heuristic, quiescence
  with delta pruning. Futility pruning excludes promotions.
- Dynamic contempt (-40) and adjudication magnet for the 200-ply rule.
- Passed pawn: tiered bonus, halved if the square ahead is blocked.
- Fixed node budget NL=150000, no clock, no randomness — deterministic.

## Files

- `main.py` — the engine (loader + LZMA blob). The only file the game runs.
- `engine.py` — readable engine source (build input, not run directly).
- `pack.py` — minifies `engine.py`, LZMA-packs it into `main.py`.
- `LICENSE` — MIT.

## Build

Run `pack.py` (needs `python-minifier` in the venv). It grid-searches LZMA
settings and writes the smallest blob into `main.py`.

## Verification

P0 correctness (measured 19 Nov 2026, local):

- perft startpos d4 = 197281, kiwipete d4 = 4085603, pos3 d4 = 43238.
- hash: 100 random walks, 0 mismatch. Eval incremental: 0 mismatch.
- mate-in-1 found (a1a8). Root startpos deterministic 2x, max 2.9 s/move.

Trial-0 (local, kit env server):

- 110k nodes: Elo 1545, 4-1-1, spare 359. Won depth-2/3/4 and 250k;
  drew 100k (threefold), lost 500k (checkmate).
- 200k nodes: Elo 1451, 4-0-2, spare 559. Lost 100k and 500k.
- The 200k regression pointed at a transposition-table flag bug
  (exact scores stored as upper bounds); fixed and re-testing.
- 200k nodes + TT fix: Elo 1545, 4-1-1, spare 475. Game 4 improved
  loss -> adjudicated draw (200 plies); game 6 still lost to 500k.
  Target Elo >=1800 NOT reached after 2 revision rounds — see report.

Step 1 — search bug hunt (19 Nov 2026, 3-step precision plan):

- Diagnosis: LMR had no re-search (reduced-depth result used as-is).
  Added LMR re-search (re-search at full depth if reduced move beats
  alpha). TT mate handling verified correct; NMP verified fine.
- Result: trial-0 UNCHANGED at Elo 1545, 4-1-1, spare 475 (byte
  identical games). LMR was not the Elo bottleneck — the eval is.
- Root cause (eval): pack.py `enc()` reuses the MG table for EG for
  P,N,B,R,Q (only the king gets a distinct EG table `E`). The tapered
  eval is effectively MG-only for most pieces.

Step 2 — node-budget calibration (19 Nov 2026):

- NL 200k -> 250k: trial-0 Elo 1545 -> 1809 (+264), 5-1-0, spare 389.
  Beat 100k (was draw), drew 500k (was loss). Trial-1 1654 (5-0-1),
  trial-2 1545 (4-1-1). Mean 1669. Still below the 2000 gate.
- NL 250k -> 300k: trial-0 Elo 1809 UNCHANGED (spare 389 -> 465);
  trial-1 Elo 1654 -> 1545 REGRESSION (depth-4 win -> threefold draw).
  Deeper search with this eval hurts. Reverted to NL=250k.
- Conclusion: node budget plateaus at 250k. The eval (standard PeSTO,
  EG=MG) caps the engine near mean 1669; the 2000 gate needs a tuned
  eval that this clean-room build cannot reproduce without copying
  the old tables. NOT submitted — gate not met.

## Surgical fix cycle 2 (20 Nov 2026, user GAS 08:15 WIB)

- (1) Removed the 78-square ev() loop: incremental 64-bit pawn
  bitboards WP/BP + bishop counts BC, KG=BD+RD at module level.
  NPS dropped to ~43k (bitboards are slower in Python than the loop),
  so NL stayed at 150000 (250k worst-case 8.73 s/move, too close to
  the 10 s limit). (2) Symmetric quantization //32 -> round-to-nearest
  //16 (offset +64 so all table chars stay printable). pack.py uses
  rename_globals=False (python_minifier rename_globals is broken:
  it produces colliding renames); the size was recovered by manual
  single-letter renames of globals/functions instead. (3) Futility
  pruning excludes pawn promotions; passed pawn bonus halved when
  the square directly ahead is occupied. Rep stays -40.
- Cycle 1: main.py 4079 B, NL=180000. Trial-0 1451 (4-0-2, one game
  abandoned by the runner), trial-1 1654 (5-0-1). Mean <1900 — failed.
- Cycle 2: restored the killer guard, NL 180000 -> 150000, main.py
  4093 B. Trial-0 2112 PERFECT (6-0-0, spare 673), trial-1 2112
  PERFECT (6-0-0, spare 733), trial-2 2112 PERFECT (6-0-0, spare 689).
  Mean 2112 (18-0-0) — gate mean >=2000 PASSED.
- Gauntlet vs nodes-1M/2M (12 games): 7-2-3 (8 points). 1M: 4-1-1,
  2M: 3-1-2. Gate gauntlet >=7/12 PASSED.

## Final metrics

- `main.py`: 4093 bytes (limit 4096, 3 bytes spare).
- Node budget: 150000. P0: perft 197281/97862/2812/9467, hash/eval
  0 mismatch, mate-in-1 99999.
- Trials (NL=150k): trial-0 2112 (6-0-0), trial-1 2112 (6-0-0),
  trial-2 2112 (6-0-0). Mean 2112. Gate mean >=2000 PASSED.
- Gauntlet 1M/2M: 7-2-3 (8 points). Gate >=7/12 PASSED.
- Ready for submit #1/3 pending makefun check green
  (thinking_reproduces >=30%, thinking_revised PASS, license_osi PASS).

## Precision surgery cycle (19 Nov 19:44 WIB, user order: do NOT submit 1669)

- (a) TT cutoff on PV-node disabled: `if de>=d and not pv:` — PV-node
  uses TT move only for ordering. (b) 2-fold repetition in search path:
  global `Q=[]`; `make()` appends parent Z, `unmake()` pops; srch
  returns -40 if `Z in HIST or Z in Q`. (c) Move ordering verified
  (TT move -> MVV-LVA -> 2 killers -> history); NMP guards verified
  (`not pv`, `d>=3`, `not inchk`, `Y>4` excludes pawn-only). P0 passed.
- Golf: TT-move ordering simplified (init `bm=0`, single sort key
  `(m==bm,mo(m))`) — freed ~45 minified bytes.
- Eval: passed-pawn bonus in EG added to `ev()` — pawns on rank 7
  (white) / rank 2 (black) get +50/-50 into EG term `d` before taper.
  King exposure penalty NOT added: no byte room (15 B spare) and the
  K MG PST already penalises central king (-40..-50); a runtime shield
  scan would cost 60+ bytes and slow every leaf eval.
- Repack: main.py still 4081 B (filter (2,0,0,64), min 10961). P0 passed.
- Trials NL=250k AFTER (a)+(b)+passed-pawn: trial-0 1809 (5-1-0,
  spare 389), trial-1 1654 (5-0-1, spare 468), trial-2 1545 (4-1-1,
  spare 311). ALL BYTE-IDENTICAL to before the fixes. Mean 1669.
  The fixes and the rank-7 passed-pawn bonus had ZERO effect on play.
- NL=300k re-test (trial-1, the regression case): 1654 (5-0-1,
  spare 468) — NO LONGER REGRESSES (was 1545 before the fixes).
  The search fixes cured the deeper-search regression, but NL300k
  adds no Elo over NL250k. Reverted to NL=250000.
- HARD GATE: mean 1669 < 2000 (gap -331). Gauntlet NOT run.
  NOT SUBMITTED, per user order. STOP.
