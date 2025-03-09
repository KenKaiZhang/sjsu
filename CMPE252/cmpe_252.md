# CMPE 252

## Graphs

**node/vertices** : unit that represents an entity, object, or data point

**edge** : connection between nodes

**path** : sequence of distinct adjacent nodes

**neighbor** of a node : another node that is directly connected to it

### Undirected Graphs

**_Graphs built upon a finite set of vertices and edges_**

types of undirected graphs

- complete graphs : every pair of distinct vertices is connected by an edge

```
(A)---(B)
 | \   |
 |  \  |
 |   \ |
(C)---(D)
```

- path graphs : consists of vertices arranged in a straight line
```
(A)---(B)---(C)---(D)---(E)
```
- cycle graphs : closed loop where each vertex has EXACTLY two neighbors
```
(A)---(B)
 |     |
(E)---(C)
  \   /
   (D)
```
- star graphs : one central vertex connected to all other vertices
```
     (A)
     /|\
    / | \
(B)  (C)  (D)
     (E)
```
- tree graphs : exactly one path between any two vertices
```
      (A)
     /   \
   (B)   (C)
  /   \     \
(D)   (E)   (F)
```

**bipartite graphs** : vertices divided into two sets with edges between the sets
```
(A)   (B)   (C)
 |     |     |
 |     |     |
(X)---(Y)---(Z)
```

### Spanning Graphs

_**Subgraph that includes all the vertices of the original graph while being connected**_

```
(A)---(B)       (A)---(B)
 |   / |         |
 |  /  |    ->   |
 | /   |         |    
(C)---(D)       (C)---(D)
```

Types of spanning subgraphs

- spanning tree : minimal connected subgraph of a graph that contains all its vertices but has no cycles (has $n - 1$ edges where $n$ is the number of nodes )
    - graph is **connected** if a spanning tree exists on the graph

**non-spanning subgraph** : subgraph that DOES NOT include all the vertices of the original graph

- a subset of the original but will exclude some vertices

### Directed Graphs

_**Graphs where the edges are given directions**_

characteristics of a directed graph

- tail : the starting vertex $\mathbf{u}$
- head : the ending vertex $\mathbf{v}$
- path : sequence of edges where each edge's head matches the next edge's tail
- adjacency : if there is a directed edge $(\mathbf{u},\mathbf{v})$, then 
    - $\mathbf{u}$ is adjacent to $\mathbf{v}$
    - $\mathbf{v}$ is not necessarily adjacent to $\mathbf{u}$
- neighborhood : set of vertices that are directly reachable from the vertex via a directed edge
    - out of $\mathbf{v}$ : set of vertices that **$\mathbf{v}$ points to**
    - in of $\mathbf{v}$ : set of vertices that **point to $\mathbf{v}$**

**subgraph**: consists of a subset of a directed graph's vertices and edges while maintaining the direction

**strongly connected** : every vertex is reachable from every other vertex via directed path

**weakly connected** : the opposite of a strongly connected graph

- only share the connected property with strongly connected if the graph is undirected 

### Laplacian Matrix

_**Matrix representation of a graph that captures its structure, connectivity, and properties**_

For a graph $G$ with $n$ vertices, its Laplacian matrix $L$ is defined as 

$$L = D - A$$

where

- $D$ = degree matrix : number of edges per vertex on the diagonal
- $A$ = adjacency matrix : shows which vertices are connected by an edge

Ex:

Given graph $G$

```
(1)---(2)
 | \   |
 |  \  |
 |   \ |
(3)---(4)
```

Then the adjacency matrix $A$ will be ...

$$
A = 
\begin{bmatrix} 
0 & 1 & 1 & 1 \\  
1 & 0 & 0 & 1 \\ 
1 & 0 & 0 & 1 \\
1 & 1 & 1 & 0
\end{bmatrix}
$$

... and the degree matrix $D$ will be ...

$$
D = 
\begin{bmatrix} 
3 & 0 & 0 & 0 \\  
0 & 2 & 0 & 0 \\ 
1 & 0 & 2 & 0 \\
0 & 0 & 0 & 3
\end{bmatrix}
$$

... therefore the Laplacian Matrix $L$ is ...

$$
L = 
D - A =  
\begin{bmatrix} 
3 & -1 & -1 & -1 \\  
-1 & 2 & 0 & -1 \\ 
-1 & 0 & 2 & -1 \\
-1 & -1 & -1 & 3
\end{bmatrix} =
0
$$

## A* Algorithm

**open lists (frontiers) & closed lists** : list containing nodes yet to be explored and nodes explored

- Dijkstra : expand frontier that is closest to $x_0$
- A* : expand frontier determined by the heuristic

**heuristic** : problem-solving approach that uses an estimate to guide decision making (efficiency > optimality)

**admissible heuristic** : satisfies ...

$$h(x_j) ≤ h^*(x_j)$$

... where ...

- $h(x_j)$ : the estimated cost from node $x_j$ to the goal
- $h^*(x_j)$ : the true cost from $x_j$ to the goal

**consistent heuristic** : if ...

$$h(x_i) <= C(x_i, x_j) + h(x_j); h(x_G) = 0$$

... and at the goal node ...

$$h(x_G) = 0$$

If $h(x)$ is both admissible and consistent, A* is guaranteed to find the optimal solution efficiently

**good heuristic** : 

- underestimate & satisfy triangle inequality
- heuristic is close to actual estimate = fast algorithm
- heuristic is close to 0 = slow algorithm

$h(x_i)$ = 0 = Dijkstra

---

**A\* Algorithm in a Nutshell** :

**1. Initialize** :

- Define the **open list** $O = \{x_o\}$ (starting node).
- Define the **closed list** $C = \{\}$ (empty set).
- Set the cost-to-come for the start node: $V(x_o) = 0$.
- Set the cost-to-come for all other nodes: $V(x_i) = \infty$.

**2. Repeat until the goal node $X_G$ is in the closed list $C$** :

- Select the node $x_j$ from $O$ with the **lowest total cost** (cost-to-come + heuristic).
- Remove $x_j$ from $O$ and add it to $C$ (mark it as explored).
- For each **neighbor $x_i$ of $x_j$** that is **not in $C$**:
  - Compute the new potential cost-to-come:  
    $V_{\text{new}} = C(x_j, x_i) + V(x_j)$
  - If $V_{\text{new}}$ is **lower** than the current $V(x_i)$, update $V(x_i)$.
  - If $x_i$ is not already in $O$, add it to $O$ (mark it for exploration).

---

Analyzing algorithms involve 3 factors :

- **completeness** : finds the optimal solution in finite time (if a solution exists)
  - DP
  - Dijkstra
  - A*
- **optimality** : finds a solution whose cost is the minimum/maximum
  - DP
  - Dijkstra
  - A*
- **efficiency** : finds the solution in the least possible time for all inputs
  - Dijksta and A* if no heuristic
  - A* with any admissible heuristic

**weighted A\*** : a variation of the A* search algorithm that prioritizes speed over optimality by using a weight to emphasize the heuristic function

---

**Weighted A\* Algorithm in a nutshell** :

**1. Initialize** :
- Define the **open list** $O = \{x_o\}$ (starting node).  
- Define the **closed list** $C = \{\}$ (empty set).  
- Set the **cost-to-come** for the start node: $V(x_o) = 0$.  
- Set the **cost-to-come** for all other nodes: $V(x_i) = \infin$.  

**2. Repeat until the goal node $X_G$ is in the closed list $C$** :
- Select the node $x_j$ from $O$ with the **lowest weighted total cost**:  
  $$  
  f_w(x_j) = V(x_j) + w \cdot h(x_j)  
  $$  
  where $w > 1$ is the weight.  
- Remove $x_j$ from $O$ and add it to $C$ (mark it as explored).  
- For each **neighbor $x_i$ of $x_j$** that is **not in $C$**:  
  - Compute the new potential cost-to-come:  
    $$  
    V_{\text{new}} = C(x_j, x_i) + V(x_j)  
    $$  
  - If $V_{\text{new}}$ is **lower** than the current $V(x_i)$, update $V(x_i)$.  
  - If $x_i$ is not already in $O$, add it to $O$ (mark it for exploration).  

---

The only difference is in the selection of $x_j$ where in A* we do ...

$$f(x) = V(x) + h(x)$$

... but in weighted A* we do ...

$$f_w(x) = V(x) + w * h(x)$$

... making the algorithm greedy and faster, but less optimal

We cannot guarantee optimality with weighted A*, but we can guarantee that it will find a path whose cost is no more than $\in$ times the minimum cost path

**anytime algorithm** : will return a good solution when being stop at any point in time

- more time == more optimal solution
- DP, Dijksta, and A* are not anytime algorithms

## Dynamic Programming

**optimal sub-structure** : property of a problem that allows it to be broken down into smaller subproblems which can be solved optimally to find the optimal solution

**Claim** :

If $ABE$ is the optimal path from $A$ to $E$, then $be$ is the optimal path from $B$ to $E$

**Proof by Contradiction** : 

1. Assumptions :
    - $ABE$ is **optimal path**
    - $BE$ is **not optimal**, thus there exists a shorter path $BXE$ such that :
$$d(BXE) < d(BE)$$

2. Proof :

    - Since $ABE$ consists of the subpath $BE$, we can replace $BE$ with $BXE$ to get the new theoretical optimal path $ABXE$
    - The total length of the new path will be :
        $$d(AB) + d{BXE}$$
    - Since we assumed that $d(BXE) < d(BE)$, this implies :
        $$d(AB) + d(BXE) < d(AB) + d(BE)$$
    - This means that for $BXE$ to be the optimal path from $B$ to $E$, the shortest path from $A$ to $E$ is $ABXE$ which contradicts our original assumption that $ABE$ is the optimal path

---

**Implementing Dynamic Programming** :

1. Assumptions :
    - $J^*_{cf}$, $J^*_{df}$ , and $J^*_{ef}$ represent the known shortest paths from nodes $c$, $d$, and $e$ to $f$

2. Problem : We want the optimal path from $b$ to $f$ where $b$ has a path to $c$, $d$, and $e$ with costs $J^*_{bc}$, $J^*_{bd}$ , and $J^*_{be}$ respectively

3. Optimal Substructure Property :
    - The optimal path cost from $b$ to $f$ :
      $$J^*_{bf} = min(J_{bc} + J^*_{cf}, J_{bd} + J^*_{df}, J_{be} + J^*_{ef})$$

4. Process 3 can be repeated into previous nodes before $b$

---

Dynamic programming is meant to reflect multistage planning over a single static choice

**memorization** : recording solutions of sub-problems (a memo)

**Bellman equation** : fundamental recursive equation describing how to break a problem into smaller sub-problems and solving it recursively

$$V(x_i) = \min_{x_j in N(x_i)}\{C(x_i,x_j) + V(x_j)\}$$
$$V(x_G) = 0$$

- $C(x_i, x_j)$ : cost of edge from $x_i$ to $x_j$
  - if no edge then $C(x_i, x_j) = inf$
- $V(x_i)$ : cost to go from x_i to x_G
  - **value function** : the minimum cost to reach the goal node from any node
- $N(x_i)$ : vertices that are outgoing neighbors of $x_i$

---

**Using Bellman Equation** :

1. Assume 
    - **Nodes** : $x_i \in \{ A, B, C, D, G \}$
    - **Edges** :
      - $C(A, B) = 1$
      - $C(A, C) = 4$
      - $C(B, C) = 2$
      - $C(B, D) = 5$
      - $C(C, D) = 1$
      - $C(D, G) = 3$
    - **Goal Node** : $ x_G = G $, so $ V(G) = 0 $.

2. We recursively compute the value function $V(x_i)$ for each node.
    - $V(D)$
      $$V(D) = \min_{x_j \in N(D)} \{ C(D, x_j) + V(x_j) \}$$
      $$V(D) = C(D, G) + V(G) = 3 + 0 = 3$$
    - $V(C)$
      $$V(C) = \min_{x_j \in N(C)} \{ C(C, x_j) + V(x_j) \}$$
      $$V(C) = C(C, D) + V(D) = 1 + 3 = 4$$
    - $V(B)$
      $$V(B) = \min_{x_j \in N(B)} \{ C(B, x_j) + V(x_j) \}$$
      $$V(B) = \min \{ C(B, C) + V(C), C(B, D) + V(D) \}$$
      $$V(B) = \min \{ 2 + 4, 5 + 3 \} = \min \{ 6, 8 \} = 6$$
    - $V(A)$
      $$V(A) = \min_{x_j \in N(A)} \{ C(A, x_j) + V(x_j) \}$$
      $$V(A) = \min \{ C(A, B) + V(B), C(A, C) + V(C) \}$$
      $$V(A) = \min \{ 1 + 6, 4 + 4 \} = \min \{ 7, 8 \} = 7$$

3. Results
    - $V(G) = 0$
    - $V(D) = 3$
    - $V(C) = 4$
    - $V(B) = 6$
    - $V(A) = 7$

Through the results, we know the **shortest path** is $ABCDG$

---

Computational cost of value function : 

- $|V|$ : number of nodes in the graph
- $\Delta$ : maximum degree of a vertex (maximum outgoing edges)

... thus :

- $|V| x |V|$ entries in the table
- comparisons per entry : $|V|^2\Delta$ 
- operations : $|V|^3$

_Ex_ : a d-dimensional grid will lead to a $n^{3d}$ complexity

## Linear/Integer Programming

Finding the optimal solution to a linear problem with constraints on inequality and equality

- Integers will only have integer values
- Linear can be any real number

---

**Miller-Tucker-Zemlin (MTZ) ILP** : formulation of the traveling salesperson problem

1. Objective : minimize the total travel cost $c_{ij}$

  $$\min\sum^{n}_{i=0}\sum^{n}_{j≠0}c_{ij}x_{ij}$$

2. Constraints
    - Binary : $x_{ij}$ has to be between 0,1
      $$0 ≤ x_{ij} ≤ 1 \qquad i,j = 0, ..., n$$
    - Flow : each city is to be only visited once
      $$\sum^{n}_{i=0,i≠j}x_{ij} = 1 \qquad j = 0, ..., n$$ 
      $$\sum^{n}_{j=0,j≠i}x_{ij} = 1 \qquad i = 0, ..., n$$ 
    - MTZ : ensures no sub-tours (there will only be one single loop)
      $$u_i \in \Z \qquad i = 0, ..., n$$
      $$u_i - u_j + nx_{ij} ≤ n - 1 \qquad 1 ≤ i ≠ j ≤ n$$

---

MTZ is for efficient for small problems, but scales poorly for large $n$

**approximates solution** : solution to an optimization problem that is "good enough" within a given bound

**approximation ratio** : how close an approximate solution is to the optimal solution

$$Approximation\,Ratio = \frac{Cost\,of\,Approximate\,Solution}{Cost\,of\,Optimal\,Solution}$$

- $Ratio = 1$ : optimal solution

Assume 

- $P$ : approximates solution
- $P^*$ : optimal solution
- $\alpha$ : approximation ratio

... then $cost(P) \le \alpha * cost(P^*)$

- $2\alpha$ : if the true solution is 100 miles, we will guarantee an approximate solution with cost at most 200 miles

---

**MST-based Approximation Algorithm for TSP**

Leveraging MST to find a suboptimal but reasonably good solution to the computationally expensive TSP solution

1. Construct an MST using Prim's or Kruskal's algorithm
```
 (A)
  |
  2
  |
 (B)
  |
  4
  |
 (C) -- 3 -- (E) 
  |
  3
  |
 (D)
```

2. Perform depth-first search (DFS) on the MST
    - Build up a path as you visit nodes in the MST
    - List nodes visited in order (allow revisit)
$$A,B,C,D,C,E,C,B,A$$

3. Skip vertices already visited
    - Use edges not included in MST when skipping

---