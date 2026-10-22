"""Edmonds' blossom algorithm for maximum cardinality matching in general graphs, O(V^3)."""
from collections import deque


def max_matching(n, edges):
    """Return a list of matched pairs (u, v), u < v, of maximum size.

    n: number of vertices labelled 0..n-1. edges: iterable of (u, v).
    """
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    match = [-1] * n
    p = [-1] * n
    base = list(range(n))

    def lca(a, b):
        seen = [False] * n
        while True:
            a = base[a]
            seen[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if seen[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, child, blossom):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = child
            child = match[v]
            v = p[match[v]]

    def find_path(root):
        nonlocal p, base
        used = [False] * n
        p = [-1] * n
        base = list(range(n))
        used[root] = True
        q = deque([root])
        while q:
            v = q.popleft()
            for to in adj[v]:
                if base[v] == base[to] or match[v] == to:
                    continue
                if to == root or (match[to] != -1 and p[match[to]] != -1):
                    cur = lca(v, to)
                    blossom = [False] * n
                    mark_path(v, cur, to, blossom)
                    mark_path(to, cur, v, blossom)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[to] == -1:
                    p[to] = v
                    if match[to] == -1:
                        return to
                    used[match[to]] = True
                    q.append(match[to])
        return -1

    # greedy warm start
    for u in range(n):
        if match[u] == -1:
            for v in adj[u]:
                if match[v] == -1:
                    match[u], match[v] = v, u
                    break
    for root in range(n):
        if match[root] == -1:
            v = find_path(root)
            while v != -1:
                pv = p[v]
                ppv = match[pv]
                match[v], match[pv] = pv, v
                v = ppv
    return sorted((u, match[u]) for u in range(n) if match[u] > u)
