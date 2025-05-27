<<<<<<< HEAD
import sys

def main(lines):
    a = 098
    print(type(a))

    for i, v in enumerate(lines):
        print("line[{0}]: {1}".format(i, v))

if __name__ == '__main__':
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    main(lines)
    
=======
import heapq
import sys

def dijkstra(n, edges, start):
    # 隣接リストの作成
    graph = [[] for _ in range(n)]
    for u, v, cost in edges:
        graph[u].append((v, cost))
    
    # 最短距離を格納（初期値は∞）
    dist = [float('inf')] * n  #[inf, inf, inf, inf, inf, inf]
    dist[start] = 0  #[0, inf, inf, inf, inf, inf]
    
    # 優先度付きキュー（最短距離が小さい順に処理）
    heap = [(0, start)]  # (距離, ノード)
    
    while heap:
        cur_dist, u = heapq.heappop(heap)
        print(cur_dist, u)
        
        # すでにもっと短い距離で訪れているなら無視（＝ループを防ぐ）
        if cur_dist > dist[u]:
            continue
        
        for v, cost in graph[u]:
            if dist[v] > dist[u] + cost:
                dist[v] = dist[u] + cost
                heapq.heappush(heap, (dist[v], v))
    
    return dist

def main():
    lines = sys.stdin.read().strip().split('\n')
    n, m, start = map(int, lines[0].split())
    edges = [tuple(map(int, line.split())) for line in lines[1:]]

    result = dijkstra(n, edges, start)
    for d in result:
        print(d)

if __name__ == "__main__":
    main()
>>>>>>> cf436f36b2ff5f26e2e3542dd9d2e5b031dd1bac
