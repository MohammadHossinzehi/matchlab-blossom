"""Hopcroft-Karp maximum bipartite matching plus Koenig minimum vertex cover."""
from collections import deque


def hopcroft_karp(n_left, n_right, edges):
    """Return (size, match_left) where match_left[u] is the right partner or -1."""
    adj = [[] for _ in range(n_left)]
    for u, v in edges:
        adj[u].append(v)
    ml = [-1] * n_left
    mr = [-1] * n_right
    INF = float("inf")

    def bfs():
        dist = [INF] * n_left
        q = deque()
        for u in range(n_left):
            if ml[u] == -1:
                dist[u] = 0
                q.append(u)
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                w = mr[v]
                if w == -1:
                    found = True
                elif dist[w] == INF:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return found, dist

    def dfs(u, dist):
        # iterative DFS to avoid recursion limits
        stack = [(u, iter(adj[u]))]
        path = []
        while stack:
            x, it = stack[-1]
            advanced = False
            for v in it:
                w = mr[v]
                if w == -1:
                    path.append((x, v))
                    for a, b in path:
                        ml[a] = b
                        mr[b] = a
                    return True
                if dist[w] == dist[x] + 1:
                    path.append((x, v))
                    stack.append((w, iter(adj[w])))
                    advanced = True
                    break
            if not advanced:
                dist[x] = INF
                stack.pop()
                if path:
                    path.pop()
        return False

    size = 0
    while True:
        found, dist = bfs()
        if not found:
            break
        for u in range(n_left):
            if ml[u] == -1 and dfs(u, dist):
                size += 1
    return size, ml


def min_vertex_cover(n_left, n_right, edges):
    """Koenig's theorem: return (left_cover, right_cover) with size == max matching."""
    size, ml = hopcroft_karp(n_left, n_right, edges)
    adj = [[] for _ in range(n_left)]
    for u, v in edges:
        adj[u].append(v)
    mr = [-1] * n_right
    for u, v in enumerate(ml):
        if v != -1:
            mr[v] = u
    zl, zr = set(), set()
    q = deque(u for u in range(n_left) if ml[u] == -1)
    zl.update(q)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v != ml[u] and v not in zr:
                zr.add(v)
                w = mr[v]
                if w != -1 and w not in zl:
                    zl.add(w)
                    q.append(w)
    left = sorted(set(range(n_left)) - zl)
    return left, sorted(zr)
