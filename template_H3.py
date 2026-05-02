# Do not change the filename or function headers
# You are free to add helper functions
# You will only have 5 attempts to run the autograder

import numpy as np
from timeit import default_timer as timer
from collections import deque
import sys
import heapq

### PREDEFINED CLASSES - DO NOT EDIT ###

# A class for undirected graph object for Q1-Q2
class UGraph:
    def __init__(self, edges, n):
        # A list of lists to represent an adjacency list
        self.adjList = [[] for _ in range(n)]

        # add edges to the undirected graph
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.adjList[dest].append(src)

# A class for directed graph object for Q3 and Q4
class DGraph:
    def __init__(self, edges, n):

        # A list of lists to represent an adjacency list
        self.adjList = [[] for _ in range(n)]

        # add edges to the directed graph
        for (src, dest) in edges:
            # add an edge from source to destination
            self.adjList[src].append(dest)

### END OF PREDEFINED CLASSES ###


# ============================================================================
# Q1. Depth-First Search (DFS)
# ============================================================================
# DFS starts at node 0 and explores as far as possible along each branch
# before backtracking. Traversal order follows the adjacency list order.

# function header for Q1.1 (Auto & manual grading)
# Recursive implementation of DFS.
# graph  -> UGraph object (adjacency list representation)
# N      -> integer, number of vertices
# return -> list of vertices in DFS exploration order, e.g., [0, 1, 2, 3, 6, 9, ...]
#
# Include comments on key lines of code (for, while, if, etc.) to demonstrate
# your comprehension of the implementation.
#
# AI Tool Used: ChatGPT
# Interaction: I asked for help identifying syntax issues in my recursive DFS and how to structure a nested helper function correctly while keeping my original approach.
# Verification: I manually checked the recursion flow, confirmed the traversal begins from node 0, and tested the function on small graphs including disconnected cases.
def q1_1(graph: UGraph, N):
    visited = [False] * N      # keep track of visited vertices
    order = []                 # store DFS exploration order

    def DFS_Recursive(s):
        visited[s] = True      # mark current node as visited
        order.append(s)        # record current node

        # visit neighbors in adjacency-list order
        for v in graph.adjList[s]:
            if visited[v] == False:
                DFS_Recursive(v)

    # start DFS from node 0 as required
    if N > 0 and not visited[0]:
        DFS_Recursive(0)

    # then continue with any unvisited vertices
    for i in range(N):
        if visited[i] == False:
            DFS_Recursive(i)

    return order


# function header for Q1.2 (Auto & manual grading)
# Iterative implementation of DFS (using an explicit stack).
# graph  -> UGraph object (adjacency list representation)
# N      -> integer, number of vertices
# return -> list of vertices in DFS exploration order, e.g., [0, 1, 2, 3, 6, 9, ...]
#
# Include comments on key lines of code to demonstrate your comprehension.
#
# AI Tool Used: ChatGPT
# Interaction: I asked for guidance on converting recursive DFS into iterative DFS using a stack while preserving adjacency-list order.
# Verification: I compared the output with recursive DFS on the same graph and checked disconnected and isolated-vertex cases.
def q1_2(graph: UGraph, N):
    visited = [False] * N
    order = []

    # process node 0 first, then any remaining disconnected vertices
    start_nodes = []
    if N > 0:
        start_nodes.append(0)
    for i in range(N):
        if i != 0:
            start_nodes.append(i)

    for start in start_nodes:
        if visited[start]:
            continue

        stack = [start]

        while stack:
            node = stack.pop()

            if visited[node]:
                continue

            visited[node] = True
            order.append(node)

            # push in reverse so visit order matches adjacency-list order
            for neighbor in reversed(graph.adjList[node]):
                if not visited[neighbor]:
                    stack.append(neighbor)

    return order


# ============================================================================
# Q2. Breadth-First Search (BFS)
# ============================================================================
# BFS starts at node 0 and explores all neighbors at the current depth before
# moving to the next level. Traversal order follows the adjacency list order.

# function header for Q2 (Auto & manual grading)
# Iterative implementation of BFS (using a queue).
# graph  -> UGraph object (adjacency list representation)
# N      -> integer, number of vertices
# return -> list of vertices in BFS exploration order, e.g., [0, 1, 2, 3, 6, 9, ...]
#
# Include comments on key lines of code to demonstrate your comprehension.
#
# AI Tool Used: ChatGPT
# Interaction: I asked for a review of my BFS logic and queue usage to make sure it follows adjacency-list order and starts from node 0.
# Verification: I tested the code on a small graph and checked that it explored level by level without revisiting nodes.
def q2(graph: UGraph, N):
    visited = [False] * N
    order = []
    q = deque([0])            # BFS starts from node 0
    visited[0] = True         # mark node 0 immediately so it is not enqueued twice

    while q:
        v = q.popleft()       # remove the front node from the queue
        order.append(v)

        # add all unvisited neighbors in adjacency-list order
        for neighbor in graph.adjList[v]:
            if not visited[neighbor]:
                visited[neighbor] = True
                q.append(neighbor)

    return order


# ============================================================================
# Q3. Strongly Connected Graph Check
# ============================================================================
# A directed graph is strongly connected if every vertex is reachable from
# every other vertex. You may re-use functions implemented in Q1 and Q2.

# function header for Q3 (Auto & manual grading)
# graph  -> DGraph object (adjacency list representation)
# N      -> integer, number of vertices
# return -> bool (True if strongly connected, False otherwise)
#
# Include comments on key lines of code to demonstrate your comprehension.
#
# AI Tool Used: ChatGPT
# Interaction: I asked for clarification on how to test strong connectivity efficiently using DFS and the transpose graph.
# Verification: I manually traced the algorithm on both a strongly connected directed graph and a graph that was not strongly connected.
def dfs_directed(adj, start, visited):
    visited[start] = True

    # recursively visit every node reachable from the current node
    for neighbor in adj[start]:
        if not visited[neighbor]:
            dfs_directed(adj, neighbor, visited)

def q3(graph: DGraph, N):
    if N == 0:
        return True

    visited = [False] * N
    dfs_directed(graph.adjList, 0, visited)

    # if some node cannot be reached from node 0, the graph is not strongly connected
    if not all(visited):
        return False

    # build the transpose graph by reversing every edge
    transpose = [[] for _ in range(N)]
    for u in range(N):
        for v in graph.adjList[u]:
            transpose[v].append(u)

    visited = [False] * N
    dfs_directed(transpose, 0, visited)

    # all nodes must also reach node 0 in the original graph
    return all(visited)


# ============================================================================
# Q4. Topological Sort
# ============================================================================
# Given a Directed Acyclic Graph (DAG), return vertices in topological order.
# Implement an enhanced DFS (post-order) as an auxiliary helper function.
# Traversal order follows the adjacency list order (no tie-breaking by key).

# function header for Q4 (Auto & manual grading)
# graph  -> DGraph object (adjacency list representation)
# n      -> integer, number of nodes
# return -> list of vertices in topological order, e.g., [4, 6, 2, 5, 0, 3, 1]
#
# Include comments on key lines of code to demonstrate your comprehension.
#
# AI Tool Used: ChatGPT
# Interaction: I asked how DFS post-order can be used to produce a topological ordering for a DAG.
# Verification: I checked that for every directed edge u -> v, node u appears before node v in the final result.
def topo_dfs(graph, node, visited, stack):
    visited[node] = True

    # explore all outgoing edges first
    for neighbor in graph.adjList[node]:
        if not visited[neighbor]:
            topo_dfs(graph, neighbor, visited, stack)

    # append after exploring descendants to get post-order
    stack.append(node)

def q4(graph: DGraph, n):
    visited = [False] * n
    stack = []

    # run DFS from every node in case the DAG has multiple components
    for node in range(n):
        if not visited[node]:
            topo_dfs(graph, node, visited, stack)

    # reverse post-order gives a valid topological ordering
    return stack[::-1]


# ============================================================================
# Q5. Minimum Spanning Tree — Kruskal's Algorithm
# ============================================================================
# Kruskal's algorithm greedily selects the minimum-weight edge that does not
# form a cycle, using a Union-Find (disjoint set) structure to track components.
# Edges are stored as [node1, node2, weight] with node1 < node2.

# Graph Class for Q5.1, 5.2, 5.3, 5.4
class Graph:
    def __init__(self, num_of_nodes):
        self.m_num_of_nodes = num_of_nodes
        self.m_graph = []   # list of edges: [node1, node2, weight]

    # Q5.1 — add_edge (0 points autograder / 5 points manual grading)
    # Add a weighted edge to the graph.
    # node1, node2 -> integers (node1 < node2 guaranteed by caller)
    # weight       -> integer, cost of the edge
    #
    # AI Tool Used: ChatGPT
    # Interaction: I asked for confirmation on how weighted edges should be stored for Kruskal’s algorithm.
    # Verification: I manually checked that edges were stored in the expected [node1, node2, weight] format.
    def add_edge(self, node1, node2, weight):
        self.m_graph.append([node1, node2, weight])

    # Q5.2 — find_subtree (0 points autograder / 5 points manual grading)
    # Recursively find the root of the subtree containing node i.
    # parent -> list, parent[i] = parent node of i (parent[root] == root)
    # i      -> integer, node whose root to find
    # return -> integer, root of the subtree containing i
    #
    # AI Tool Used: ChatGPT
    # Interaction: I asked how the recursive find operation works in a Union-Find structure.
    # Verification: I traced examples by hand to confirm the returned value was always the set representative.
    def find_subtree(self, parent, i):
        if parent[i] == i:
            return i
        return self.find_subtree(parent, parent[i])

    # Q5.3 — connect_subtrees (0 points autograder / 5 points manual grading)
    # Union by size: find the roots of x and y, then attach the smaller
    # subtree under the larger one to keep the tree balanced.
    # parent        -> list, parent array
    # subtree_sizes -> list, number of nodes in each subtree
    # x, y          -> integers, nodes whose subtrees to connect
    #
    # AI Tool Used: ChatGPT
    # Interaction: I asked for help implementing union by size in a way that matches Kruskal’s algorithm.
    # Verification: I manually checked that the smaller subtree was attached to the larger one and that subtree sizes updated correctly.
    def connect_subtrees(self, parent, subtree_sizes, x, y):
        root_x = self.find_subtree(parent, x)
        root_y = self.find_subtree(parent, y)

        if root_x == root_y:
            return

        # attach the smaller subtree to the larger subtree
        if subtree_sizes[root_x] < subtree_sizes[root_y]:
            parent[root_x] = root_y
            subtree_sizes[root_y] += subtree_sizes[root_x]
        else:
            parent[root_y] = root_x
            subtree_sizes[root_x] += subtree_sizes[root_y]

    # Q5.4 — MST_Kruskal (15 points autograder / 5 points manual grading)
    # Find the Minimum Spanning Tree using Kruskal's algorithm.
    # Sort all edges by weight, then greedily add edges that do not form cycles.
    # return -> list of MST edges in ascending order of their weights
    #           e.g., [[2,5],[4,5],[3,4],[5,7],[0,1],[6,8],[3,6],[0,2]]
    #
    # Ex: (graph from Figure 1 in assignment) → [[2,5],[4,5],[3,4],[5,7],[0,1],[6,8],[3,6],[0,2]]
    #
    # AI Tool Used: ChatGPT
    # Interaction: I asked for a review of the overall Kruskal workflow using sorting plus Union-Find.
    # Verification: I tested the algorithm on the sample graph and checked that the selected edges were in ascending weight order and formed no cycles.
    def MST_Kruskal(self):
        result = []
        parent = [i for i in range(self.m_num_of_nodes)]
        subtree_sizes = [1] * self.m_num_of_nodes

        # sort edges from smallest weight to largest weight
        edges = sorted(self.m_graph, key=lambda e: e[2])

        for node1, node2, weight in edges:
            root1 = self.find_subtree(parent, node1)
            root2 = self.find_subtree(parent, node2)

            # only add the edge if it connects two different components
            if root1 != root2:
                result.append([node1, node2])
                self.connect_subtrees(parent, subtree_sizes, root1, root2)

                # an MST for n nodes always contains exactly n - 1 edges
                if len(result) == self.m_num_of_nodes - 1:
                    break

        return result


# ============================================================================
# Q6. City Construction — MST Savings via Prim's Algorithm
# ============================================================================
# Given buildings and road costs, compute how much budget is saved by building
# only the MST roads instead of all roads. Must use Prim's algorithm (not
# Kruskal) for full credit.
#
# Input format (2D list):
#   input[0]: [N, M, 0]  — N buildings (3 < N ≤ 10^5), M roads, trailing 0
#   input[1..M]: [a, b, c]  — road between buildings a and b, cost c
#                             (1 ≤ a, b < N, a ≠ b, 1 ≤ c ≤ 10^6)
#   Constraints: 2 ≤ M ≤ min(N(N-1)/2, 5×10^5)
#
# return -> integer, (total road cost) - (MST cost) = savings
#           Return -1 if not all buildings are connected.
#
# Ex: input=[[5,4,0],[1,2,1],[2,3,1],[3,1,1],[4,5,5]] → -1
#
# Include comments on key lines of code to demonstrate your comprehension.
#
# AI Tool Used: ChatGPT
# Interaction: I asked how to implement Prim’s algorithm with a min-heap for a large sparse graph and how to handle malformed or mismatched row-count input safely.
# Verification: I manually tested connected and disconnected graphs and also checked cases where the number of edge rows did not match the declared M value.
def q6(input):
    if not input or len(input) == 0:
        return -1

    N = input[0][0]

    # use the actual rows provided instead of trusting M completely
    roads = input[1:]

    adj = [[] for _ in range(N + 1)]
    total_cost = 0

    # build graph from all provided road rows
    for row in roads:
        if len(row) < 3:
            continue

        a, b, c = row[0], row[1], row[2]
        adj[a].append((b, c))
        adj[b].append((a, c))
        total_cost += c

    visited = [False] * (N + 1)
    min_heap = [(0, 1)]   # start Prim from building 1
    mst_cost = 0
    visited_count = 0

    while min_heap and visited_count < N:
        cost, node = heapq.heappop(min_heap)

        if visited[node]:
            continue

        visited[node] = True
        visited_count += 1
        mst_cost += cost

        for neighbor, weight in adj[node]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (weight, neighbor))

    if visited_count != N:
        return -1

    return total_cost - mst_cost


# ============================================================================
# Q7. Small World Network
# ============================================================================
# Verify the Small World Network criterion: every pair of people must be
# reachable within at most 6 degrees of separation. Use BFS from each node
# to compute shortest paths, then check all pairwise distances.
# People are numbered 1..N.
#
# Input format (2D list):
#   input[0]: [N, K]  — N people (1 ≤ N ≤ 100), K friendships
#   input[1..K]: [A, B]  — bidirectional friendship between A and B
#                          (1 ≤ A, B ≤ N, no duplicates, no self-loops)
#
# return -> "Small World!" if all connected pairs satisfy ≤ 6 steps,
#           "Big World!" otherwise.
#
# Ex: input=[[5,5],[1,2],[2,3],[3,5],[1,4],[1,3]] → "Small World!"
#
# Approach: I used BFS starting from every person. Since the graph is unweighted,
# BFS gives the shortest number of friendship steps from one person to all others.
# If any person is unreachable or more than 6 steps away, then the network does
# not satisfy the Small World condition.
#
# Include comments on key lines of code to demonstrate your comprehension.
#
# AI Tool Used: ChatGPT
# Interaction: I asked which graph algorithm best checks whether every pair of nodes is within 6 edges in an unweighted graph and how to make the input parsing more robust.
# Verification: I tested the function on connected, disconnected, long-path, and single-node cases.
def q7(input):
    if not input or len(input) == 0:
        return "Big World!"

    first_row = input[0]

    # handle cases where only N is provided or K is inconsistent
    N = first_row[0]
    if len(first_row) >= 2:
        K = first_row[1]
    else:
        K = len(input) - 1

    # use the actual friendship rows available
    friendships = input[1:]

    adj = [[] for _ in range(N + 1)]

    for row in friendships:
        if len(row) < 2:
            continue

        a, b = row[0], row[1]
        adj[a].append(b)
        adj[b].append(a)

    # BFS from every person to check shortest path distances
    for start in range(1, N + 1):
        dist = [-1] * (N + 1)
        queue = deque([start])
        dist[start] = 0

        while queue:
            node = queue.popleft()

            if dist[node] == 6:
                continue

            for neighbor in adj[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)

        # every person must be reachable within 6 steps
        for person in range(1, N + 1):
            if dist[person] == -1 or dist[person] > 6:
                return "Big World!"

    return "Small World!"


# ============================================================================
# Main - Test Section
# ============================================================================
if __name__ == "__main__":
    print("========== Q1 / Q2 Tests ==========")
    edges_undirected = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    ugraph = UGraph(edges_undirected, 6)

    print("Q1.1 Recursive DFS:", q1_1(ugraph, 6))   # expected [0, 1, 3, 4, 2, 5]
    print("Q1.2 Iterative DFS:", q1_2(ugraph, 6))   # expected [0, 1, 3, 4, 2, 5]
    print("Q2 BFS:", q2(ugraph, 6))                 # expected [0, 1, 2, 3, 4, 5]

    print("\n========== Q3 Tests ==========")
    sc_edges = [(0, 1), (1, 2), (2, 0)]
    not_sc_edges = [(0, 1), (1, 2)]

    dgraph1 = DGraph(sc_edges, 3)
    dgraph2 = DGraph(not_sc_edges, 3)

    print("Q3 Strongly Connected (True case):", q3(dgraph1, 3))   # expected True
    print("Q3 Strongly Connected (False case):", q3(dgraph2, 3))  # expected False

    print("\n========== Q4 Tests ==========")
    dag_edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    dag = DGraph(dag_edges, 6)
    print("Q4 Topological Sort:", q4(dag, 6))
    # one valid output is [5, 4, 2, 3, 1, 0]

    print("\n========== Q5 Tests ==========")
    g = Graph(9)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 7)
    g.add_edge(1, 2, 11)
    g.add_edge(1, 3, 9)
    g.add_edge(1, 5, 20)
    g.add_edge(2, 5, 1)
    g.add_edge(3, 6, 6)
    g.add_edge(3, 4, 2)
    g.add_edge(4, 6, 10)
    g.add_edge(4, 8, 15)
    g.add_edge(4, 7, 5)
    g.add_edge(4, 5, 1)
    g.add_edge(5, 7, 3)
    g.add_edge(6, 8, 5)
    g.add_edge(7, 8, 12)

    print("Q5 MST Kruskal:", g.MST_Kruskal())
    # expected [[2,5],[4,5],[3,4],[5,7],[0,1],[6,8],[3,6],[0,2]]

    print("\n========== Q6 Tests ==========")
    city1 = [
        [6, 8, 0],
        [1, 2, 3],
        [1, 3, 5],
        [2, 3, 1],
        [2, 4, 4],
        [3, 5, 6],
        [4, 5, 2],
        [4, 6, 7],
        [5, 6, 1]
    ]
    city2 = [
        [5, 4, 0],
        [1, 2, 1],
        [2, 3, 1],
        [3, 1, 1],
        [4, 5, 5]
    ]

    print("Q6 Savings (connected graph):", q6(city1))
    print("Q6 Savings (disconnected graph):", q6(city2))   # expected -1

    print("\n========== Q7 Tests ==========")
    small_world_input = [
        [5, 5],
        [1, 2],
        [2, 3],
        [3, 5],
        [1, 4],
        [1, 3]
    ]

    big_world_input = [
        [8, 7],
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8]
    ]  # 1 to 8 takes 7 steps, so this should fail

    print("Q7 Small World case:", q7(small_world_input))   # expected Small World!
    print("Q7 Big World case:", q7(big_world_input))       # expected Big World!