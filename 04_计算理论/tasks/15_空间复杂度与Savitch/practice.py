"""第15晚：BFS 与 Savitch 风格有界可达性。"""
from collections import deque
from math import ceil, log2

def bfs_reachable(n, edges, source, target):
    queue, seen = deque([source]), {source}
    peak = 1
    while queue:
        u = queue.popleft()
        if u == target:
            return True, peak
        for v in range(n):
            if (u,v) in edges and v not in seen:
                seen.add(v); queue.append(v)
        peak = max(peak, len(seen) + len(queue))
    return False, peak

def savitch(n, edges, u, v, k, stats, depth=0):
    stats["calls"] += 1
    stats["peak_depth"] = max(stats["peak_depth"], depth)
    if k == 0:
        return u == v or (u,v) in edges
    for middle in range(n):
        if (savitch(n,edges,u,middle,k-1,stats,depth+1)
                and savitch(n,edges,middle,v,k-1,stats,depth+1)):
            return True
    return False

if __name__ == "__main__":
    n = 7
    edges = {(0,1),(1,2),(2,3),(3,4),(4,5),(1,6)}
    k = ceil(log2(max(1,n-1)))
    for target in range(n):
        expected, bfs_peak = bfs_reachable(n,edges,0,target)
        stats = {"calls":0, "peak_depth":0}
        actual = savitch(n,edges,0,target,k,stats)
        assert actual == expected
        print(f"0->{target}: {actual}, BFS-items<={bfs_peak}, "
              f"Savitch depth={stats['peak_depth']}, calls={stats['calls']}")
    # 动手改造：加 memoization 比较时间下降与额外空间上升。
