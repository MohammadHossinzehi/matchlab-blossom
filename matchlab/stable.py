"""Stable matching: Gale-Shapley (two sided) and Irving's stable roommates."""


def gale_shapley(proposer_prefs, receiver_prefs):
    """Proposer-optimal stable matching. Prefs are lists of full rankings.

    Returns a list: partner[proposer] = receiver.
    """
    n = len(proposer_prefs)
    rank = [{r: i for i, r in enumerate(p)} for p in receiver_prefs]
    nxt = [0] * n
    holder = [-1] * n
    free = list(range(n))
    while free:
        a = free.pop()
        r = proposer_prefs[a][nxt[a]]
        nxt[a] += 1
        cur = holder[r]
        if cur == -1:
            holder[r] = a
        elif rank[r][a] < rank[r][cur]:
            holder[r] = a
            free.append(cur)
        else:
            free.append(a)
    partner = [-1] * n
    for r, a in enumerate(holder):
        partner[a] = r
    return partner


def stable_roommates(prefs):
    """Irving's algorithm. prefs[i] is a ranking of all others. Returns partner list or None."""
    n = len(prefs)
    if n % 2:
        return None
    table = [list(p) for p in prefs]
    rank = [{x: i for i, x in enumerate(p)} for p in prefs]

    def delete(a, b):
        if b in table[a]:
            table[a].remove(b)
        if a in table[b]:
            table[b].remove(a)

    # phase 1: proposals
    holds = [None] * n  # holds[x] = proposer x currently holds
    proposed_to = [None] * n
    free = list(range(n))
    while free:
        a = free.pop()
        while True:
            if not table[a]:
                return None
            b = table[a][0]
            if holds[b] is None:
                holds[b] = a
                proposed_to[a] = b
                break
            cur = holds[b]
            if rank[b][a] < rank[b][cur]:
                holds[b] = a
                proposed_to[a] = b
                proposed_to[cur] = None
                delete(cur, b)
                free.append(cur)
                break
            delete(a, b)
    for b in range(n):
        h = holds[b]
        if h is None:
            return None
        for x in list(table[b]):
            if rank[b][x] > rank[b][h]:
                delete(b, x)
    # phase 2: eliminate rotations
    while True:
        if any(len(t) == 0 for t in table):
            return None
        start = next((i for i in range(n) if len(table[i]) > 1), None)
        if start is None:
            break
        seq, pos = [], {}
        p = start
        while p not in pos:
            pos[p] = len(seq)
            seq.append(p)
            q = table[p][1]
            p = table[q][-1]
        cyc = seq[pos[p]:]
        pairs = []
        for x in cyc:
            y = table[x][1]
            pairs.append((x, y))
        for x, y in pairs:
            while table[y] and table[y][-1] != x:
                delete(y, table[y][-1])
        if any(len(t) == 0 for t in table):
            return None
    partner = [t[0] for t in table]
    if any(partner[partner[i]] != i for i in range(n)):
        return None
    return partner


def is_stable_pairing(prefs, partner):
    """True when no two people prefer each other to their assigned partners."""
    n = len(prefs)
    rank = [{x: i for i, x in enumerate(p)} for p in prefs]
    for a in range(n):
        for b in range(a + 1, n):
            if partner[a] != b and rank[a][b] < rank[a][partner[a]] and rank[b][a] < rank[b][partner[b]]:
                return False
    return True
