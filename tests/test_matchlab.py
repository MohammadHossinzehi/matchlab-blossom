import itertools
import random
import unittest

from matchlab import max_matching, hopcroft_karp, min_vertex_cover, gale_shapley, stable_roommates
from matchlab.stable import is_stable_pairing


def brute_matching(n, edges):
    edges = list({tuple(sorted(e)) for e in edges if e[0] != e[1]})
    best = 0

    def rec(i, used, cnt):
        nonlocal best
        best = max(best, cnt)
        for j in range(i, len(edges)):
            u, v = edges[j]
            if u not in used and v not in used:
                rec(j + 1, used | {u, v}, cnt + 1)

    rec(0, frozenset(), 0)
    return best


class TestBlossom(unittest.TestCase):
    def test_odd_cycle(self):
        self.assertEqual(len(max_matching(5, [(i, (i + 1) % 5) for i in range(5)])), 2)

    def test_blossom_needs_contraction(self):
        edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
        self.assertEqual(len(max_matching(4, edges)), 2)

    def test_random_vs_brute(self):
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(1, 9)
            edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.3]
            m = max_matching(n, edges)
            verts = [x for e in m for x in e]
            self.assertEqual(len(verts), len(set(verts)))
            self.assertTrue(all(e in edges for e in m))
            self.assertEqual(len(m), brute_matching(n, edges))


class TestBipartite(unittest.TestCase):
    def test_random_vs_blossom_and_koenig(self):
        rng = random.Random(2)
        for _ in range(200):
            L, R = rng.randint(1, 8), rng.randint(1, 8)
            edges = [(u, v) for u in range(L) for v in range(R) if rng.random() < 0.3]
            size, ml = hopcroft_karp(L, R, edges)
            general = max_matching(L + R, [(u, L + v) for u, v in edges])
            self.assertEqual(size, len(general))
            lc, rc = min_vertex_cover(L, R, edges)
            self.assertEqual(len(lc) + len(rc), size)
            for u, v in edges:
                self.assertTrue(u in lc or v in rc)


class TestStable(unittest.TestCase):
    def test_gale_shapley_stable(self):
        rng = random.Random(3)
        for _ in range(100):
            n = rng.randint(1, 7)
            P = [rng.sample(range(n), n) for _ in range(n)]
            Q = [rng.sample(range(n), n) for _ in range(n)]
            m = gale_shapley(P, Q)
            inv = {r: a for a, r in enumerate(m)}
            for a in range(n):
                for r in range(n):
                    if m[a] != r:
                        a_prefers = P[a].index(r) < P[a].index(m[a])
                        r_prefers = Q[r].index(a) < Q[r].index(inv[r])
                        self.assertFalse(a_prefers and r_prefers)

    def test_roommates_vs_brute(self):
        rng = random.Random(4)
        solved = 0
        for _ in range(300):
            n = rng.choice([4, 6])
            prefs = [rng.sample([j for j in range(n) if j != i], n - 1) for i in range(n)]
            exists = False
            for perm in itertools.permutations(range(n)):
                partner = [0] * n
                ok = all(perm[i] != i for i in range(n))
                if ok:
                    for i in range(n):
                        partner[i] = perm[i]
                    ok = all(partner[partner[i]] == i for i in range(n))
                if ok and is_stable_pairing(prefs, partner):
                    exists = True
                    break
            got = stable_roommates(prefs)
            self.assertEqual(got is not None, exists)
            if got is not None:
                solved += 1
                self.assertTrue(is_stable_pairing(prefs, got))
        self.assertGreater(solved, 0)

    def test_classic_unsolvable(self):
        prefs = [[1, 2, 3], [2, 0, 3], [0, 1, 3], [0, 1, 2]]
        self.assertIsNone(stable_roommates(prefs))


if __name__ == "__main__":
    unittest.main()
