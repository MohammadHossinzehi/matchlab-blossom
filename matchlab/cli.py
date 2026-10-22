"""CLI: python -m matchlab.cli blossom FILE  (FILE has 'n' then one 'u v' edge per line)."""
import sys
from .blossom import max_matching


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 2 or argv[0] != "blossom":
        print(__doc__)
        return 2
    with open(argv[1]) as f:
        toks = f.read().split()
    n = int(toks[0])
    nums = list(map(int, toks[1:]))
    edges = list(zip(nums[0::2], nums[1::2]))
    m = max_matching(n, edges)
    print(f"matching size {len(m)}")
    for u, v in m:
        print(u, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
