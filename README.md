# CS 460 — Algorithms: Homework 3

Coding assignment 3 for **CS 460: Algorithms** at San Diego State University.

**Course:** CS 460 — Algorithms  
**Institution:** San Diego State University  
**Language:** Python

---

## Problems Implemented

| # | Problem | Algorithm / Concept |
|---|---|---|
| Q1.1 | Depth-First Search — Recursive | DFS, recursion, adjacency list |
| Q1.2 | Depth-First Search — Iterative | DFS, explicit stack |
| Q2 | Breadth-First Search | BFS, deque/queue |
| Q3 | Strongly Connected Graph Check | Kosaraju's idea — DFS + transpose graph |
| Q4 | Topological Sort | DFS post-order on a DAG |
| Q5 | Minimum Spanning Tree | Kruskal's algorithm + Union-Find (union by size) |
| Q6 | City Construction — MST Savings | Prim's algorithm with min-heap |
| Q7 | Small World Network (6 degrees) | Multi-source BFS, shortest path checking |

---

## Concepts Covered

- **Graph traversal** — recursive and iterative DFS, BFS on undirected and directed graphs
- **Directed graphs** — strong connectivity via transpose + DFS, topological ordering via post-order DFS
- **Minimum Spanning Trees** — Kruskal's (sort + Union-Find) and Prim's (greedy + min-heap)
- **Shortest paths** — unweighted BFS for the small-world / 6-degrees-of-separation problem
- **Disjoint Set / Union-Find** — `find` with path compression, `union` by size

---

## File

| File | Description |
|---|---|
| `template_H3.py` | All 7 implementations with inline comments and test cases in `__main__` |

---

## How to Run

```bash
python template_H3.py
```

Requires Python 3. No external dependencies beyond the standard library (`collections.deque`, `heapq`).

---

*Part of my CS coursework at SDSU. See [algochw2](https://github.com/tngnghi/algochw2) for the previous assignment, and my [data-structure](https://github.com/tngnghi/data-structure) repo for interactive visualizations of the underlying structures.*
