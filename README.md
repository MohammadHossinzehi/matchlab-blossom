# matchlab

Matching algorithms from scratch in pure Python, with zero dependencies: Edmonds' blossom algorithm for general graphs, Hopcroft-Karp for bipartite graphs with Koenig minimum vertex covers, and stable matching via Gale-Shapley and Irving's stable roommates.

## Why

Matching is the classic problem behind assignment, scheduling, pairing students with schools and cover problems. The interesting part is that general (non-bipartite) graphs need odd cycle contraction ("blossoms"), and that stable roommates may have no solution at all. This repo implements each algorithm cleanly and checks it against exhaustive oracles.

## What is inside

| Module | Algorithm | Complexity |
| --- | --- | --- |
| `matchlab/blossom.py` | Edmonds blossom, maximum cardinality matching, general graphs | O(V^3) |
| `matchlab/bipartite.py` | Hopcroft-Karp (iterative DFS) and Koenig minimum vertex cover | O(E sqrt(V)) |
| `matchlab/stable.py` | Gale-Shapley (proposer optimal) and Irving's stable roommates | O(n^2) |
| `matchlab/cli.py` | Command line front end for the blossom matcher | |

## Run it

```bash
python3 -m unittest discover -s tests -v
```

```python
from matchlab import max_matching, hopcroft_karp, gale_shapley, stable_roommates

max_matching(4, [(0, 1), (1, 2), (2, 0), (2, 3)])   # [(0, 1), (2, 3)]
hopcroft_karp(2, 2, [(0, 0), (0, 1), (1, 0)])        # (2, [1, 0])
stable_roommates([[1, 2, 3], [2, 0, 3], [0, 1, 3], [0, 1, 2]])  # None, no stable pairing exists
```

CLI: put the vertex count on the first line, then one `u v` edge per line, and run `python3 -m matchlab.cli blossom graph.txt`.

## Design and testing notes

- The blossom implementation uses the base array and LCA contraction style, so blossoms are contracted implicitly by relabelling bases instead of building contracted graphs.
- Hopcroft-Karp uses an iterative DFS so large graphs do not hit Python's recursion limit.
- Tests compare the blossom matcher with a brute force maximum matching on 300 random graphs, verify Hopcroft-Karp agrees with the blossom matcher on random bipartite graphs, and check that Koenig covers are valid and exactly as large as the matching.
- Gale-Shapley results are checked for blocking pairs. Stable roommates is compared against exhaustive search over all pairings, including the existence/non-existence decision.
