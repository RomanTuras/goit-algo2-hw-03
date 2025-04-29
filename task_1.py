from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

N = 22  # Кількість вершин

# Створюємо матрицю пропускної здатності
capacity_matrix = [[0] * N for _ in range(N)]

# Джерело → термінали
capacity_matrix[0][1] = 60
capacity_matrix[0][2] = 55

# Термінал 1 → склади
capacity_matrix[1][3] = 25
capacity_matrix[1][4] = 20
capacity_matrix[1][5] = 15

# Термінал 2 → склади
capacity_matrix[2][5] = 15
capacity_matrix[2][6] = 30
capacity_matrix[2][4] = 10

# Склади → магазини
capacity_matrix[3][7] = 15
capacity_matrix[3][8] = 10
capacity_matrix[3][9] = 20

capacity_matrix[4][10] = 15
capacity_matrix[4][11] = 10
capacity_matrix[4][12] = 25

capacity_matrix[5][13] = 20
capacity_matrix[5][14] = 15
capacity_matrix[5][15] = 10

capacity_matrix[6][16] = 20
capacity_matrix[6][17] = 10
capacity_matrix[6][18] = 15
capacity_matrix[6][19] = 5
capacity_matrix[6][20] = 10

# Магазини → стік
for i in range(7, 21):
    capacity_matrix[i][21] = 30


# BFS пошук шляху
def bfs(capacity, flow, s, t, parent):
    visited = [False] * N
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in range(N):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == t:
                    return True
                queue.append(v)
    return False


# Алгоритм Едмондса-Карпа
def edmonds_karp(capacity, source, sink):
    flow = [[0] * N for _ in range(N)]
    parent = [-1] * N
    max_flow = 0

    while bfs(capacity, flow, source, sink, parent):
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

        max_flow += path_flow

    return max_flow, flow


# Запускаємо
source, sink = 0, 21
max_flow, flow_matrix = edmonds_karp(capacity_matrix, source, sink)

print(f"\n🔹 Максимальний потік: {max_flow} одиниць\n")
print("📦 Таблиця фактичних потоків (термінал → магазин):")

# Таблиця термінал → магазин
for term in [1, 2]:
    for store in range(7, 21):
        flow = 0
        for warehouse in range(3, 7):
            if flow_matrix[warehouse][store] > 0 and (
                capacity_matrix[1][warehouse] > 0 or capacity_matrix[2][warehouse] > 0
            ):
                flow += flow_matrix[warehouse][store]
        if flow > 0:
            print(f"Термінал {term} → Магазин {store - 6}: {flow} од.")

# Побудова графу
G = nx.DiGraph()
for i in range(N):
    for j in range(N):
        if capacity_matrix[i][j] > 0:
            G.add_edge(i, j, capacity=capacity_matrix[i][j], flow=flow_matrix[i][j])

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, node_size=900, node_color="skyblue", arrows=True)
edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color="red", font_size=9
)
plt.title("Граф потоків у логістичній мережі")
plt.show()
