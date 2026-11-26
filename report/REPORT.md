# CAPSTONE PROJECT REPORT

## DESIGN AND ANALYSIS OF ALGORITHMS (ETCCDA302)

# **MINI-COURIER DISPATCH PLANNER & ROUTE OPTIMIZATION ENGINE**

---

### **Submitted By:**
- **Student Name:** Laksh Vashist  
- **Roll Number:** 2501730202  
- **Program:** B.Tech. in Computer Science and Engineering (CSE)  
- **Institution:** K.R. Mangalam University, Gurugram  

### **Under the Guidance of:**
- **Mentor / Faculty Guide:** Ms. Ankita Singh  
  *Assistant Professor, Department of Computer Science & Engineering*  
  *School of Engineering and Technology, K.R. Mangalam University*  

---

## **DECLARATION & CERTIFICATE OF ORIGINALITY**

I, **Laksh Vashist** (Roll No: **2501730202**), student of B.Tech. Computer Science & Engineering at **K.R. Mangalam University**, hereby declare that the capstone project entitled **"Mini-Courier Dispatch Planner & Route Optimization Engine"** submitted in partial fulfillment of the academic requirements for the subject **Design and Analysis of Algorithms (ETCCDA302)** is an authentic record of my own work carried out under the supervision and guidance of **Ms. Ankita Singh**.

This work has not been submitted previously to any other university or institution for the award of any degree or diploma.

**Date:** November 2026  
**Place:** Gurugram, Haryana  

*(Laksh Vashist)*  
Roll No: 2501730202  
Department of Computer Science & Engineering  
K.R. Mangalam University  

---

## **ACKNOWLEDGEMENT**

I take immense pleasure in expressing my profound gratitude and sincere appreciation to my esteemed faculty mentor, **Ms. Ankita Singh**, Department of Computer Science and Engineering, **K.R. Mangalam University**, for her invaluable mentorship, constructive feedback, and continuous encouragement throughout the conception, analysis, and execution of this Design and Analysis of Algorithms (DAA) Capstone Project.

Her deep insights into asymptotic complexity, dynamic programming recurrence formulation, and graph heuristics have played a decisive role in shaping both the theoretical rigor and practical implementation of this project.

I would also like to express my gratitude to the **Department of Computer Science & Engineering** and the **School of Engineering and Technology, K.R. Mangalam University** for providing the academic infrastructure, laboratories, and supportive learning environment that made this work possible.

Finally, I thank my family and peers for their persistent encouragement and collaboration.

---

## **ABSTRACT**

Last-mile urban parcel delivery represents a classic NP-hard logistical challenge that involves multiple conflicting objectives: prioritizing urgent parcels, adhering strictly to vehicle payload capacities, calculating shortest travel trajectories across sparse street networks, and sequencing customer stops into an efficient closed tour.

This project, **"Mini-Courier Dispatch Planner & Route Optimization Engine"**, designs, implements, and benchmarks a multi-tier algorithmic pipeline that addresses each facet of urban dispatch planning:
1. **Urgency Sorting**: Implements a stable **Merge Sort** ($O(n \log n)$) to rank incoming parcels by composite urgency keys `(priority, deadline_hours)`.
2. **Optimal Payload Selection**: Solves the 0/1 Knapsack problem via **Dynamic Programming** ($O(n \cdot W)$) to maximize total delivery charges (revenue) without exceeding the vehicle's $25\text{ kg}$ weight limit.
3. **Shortest Metric Pathfinding**: Employs **Dijkstra’s Algorithm** with min-heap priority queues ($O((V + E) \log V)$) on an adjacency-list representation of the NCR (Gurugram) road network to build an exact metric distance matrix between all active delivery nodes.
4. **Tour Optimization**: Solves the metric Traveling Salesperson Problem (TSP) using a greedy **Nearest Neighbor Heuristic** ($O(n^2)$), benchmarked against an exact brute-force permutation search ($O(n!)$) to analyze approximation bounds.
5. **Interactive Full-Stack Architecture**: Accompanied by both a modernized Unicode/ANSI terminal interface (`main.py`) and an interactive Web Dashboard (`web/index.html` & `server.py`) with real-time road canvas rendering, animated delivery van simulation, dynamic payload sliders, and interactive DP matrices.

Theoretical asymptotic boundaries are verified via comprehensive empirical performance benchmarks across small, medium, and large input scales.

---

## **TABLE OF CONTENTS**

1. [Introduction and Problem Definition](#1-introduction-and-problem-definition)
2. [Project Objectives and Scope](#2-project-objectives-and-scope)
3. [System Architecture and Data Flow](#3-system-architecture-and-data-flow)
4. [Data Representation and Mathematical Formulations](#4-data-representation-and-mathematical-formulations)
5. [Detailed Algorithmic Analysis](#5-detailed-algorithmic-analysis)
   - 5.1 Urgency Ordering via Stable Merge Sort
   - 5.2 Optimal Payload Selection via 0/1 Knapsack Dynamic Programming
   - 5.3 Metric Shortest Paths via Dijkstra's Algorithm
   - 5.4 Tour Construction via Nearest Neighbor TSP vs. Brute-Force
6. [Frontend & Interactive Dashboard Design](#6-frontend--interactive-dashboard-design)
7. [Comprehensive Asymptotic Complexity Analysis](#7-comprehensive-asymptotic-complexity-analysis)
8. [Sample Execution Walkthrough and Verification](#8-sample-execution-walkthrough-and-verification)
9. [Empirical Benchmarks and Runtime Analysis](#9-empirical-benchmarks-and-runtime-analysis)
10. [Limitations, Bottlenecks, and Future Scope](#10-limitations-bottlenecks-and-future-scope)
11. [Viva Voce Technical Preparation](#11-viva-voce-technical-preparation)
12. [Conclusion](#12-conclusion)
13. [References & Execution Guidelines](#13-references--execution-guidelines)

---

## 1. Introduction and Problem Definition

In modern logistics and smart-city dispatch networks, couriers face constrained transport conditions where order volume exceeds vehicle carrying capacity, deadlines vary across customer tiers, and local traffic maps consist of irregular, non-complete road networks. 

To plan an optimal single-vehicle dispatch trip from a central warehouse, four foundational algorithmic questions must be answered sequentially:
1. **Prioritization**: When dozens of parcels are queued, how do we order them by strict delivery SLA (service level agreement) without perturbing equal-tier customer requests?
2. **Capacity Optimization**: Since the delivery vehicle has a strict weight limit $W = 25\text{ kg}$, which subset of discrete parcels yields the maximum monetary revenue?
3. **Metric Road Distance**: Because cities do not have direct road connections between every pair of locations, how do we determine the shortest physical road distances and reconstruct turn-by-turn routes?
4. **Tour Sequencing**: In what sequence should the selected delivery locations be visited such that total trip distance is minimized and the courier returns to the warehouse?

The **Mini-Courier Dispatch Planner** models these four interconnected problems into a unified pipeline where the output of each algorithmic stage forms the input to the next.

---

## 2. Project Objectives and Scope

The primary objectives established for this DAA Capstone project are:
- **Design and Model Real-World Data**: Create JSON-based schemas representing physical road networks $G = (V, E)$ and parcel inventories with multi-attribute constraints.
- **Implement Core DAA Algorithms**:
  - Implement $O(n \log n)$ stable Merge Sort and compare against $O(n^2)$ Bubble Sort.
  - Implement 0/1 Knapsack Dynamic Programming with table memoization and backtracking.
  - Implement Dijkstra's algorithm with min-heap priority queues for all-pairs distance extraction.
  - Implement Nearest Neighbor heuristic approximation for TSP and evaluate its approximation ratio against exact brute-force search.
- **Deliver Modern User Interfaces**:
  - Develop a terminal CLI featuring Unicode box-drawing tables, payload progress meters, and color-coded status badges.
  - Develop a zero-dependency interactive Web Dashboard with HTML5 Canvas road network rendering, animated courier pathing, and real-time Knapsack slider controls.
- **Empirical Complexity Benchmarking**: Evaluate wall-clock runtime across small, medium, and large synthetic datasets to corroborate theoretical asymptotic growth orders $\mathcal{O}(n \log n)$, $\mathcal{O}(n \cdot W)$, $\mathcal{O}((V + E) \log V)$, and $\mathcal{O}(n^2)$.

---

## 3. System Architecture and Data Flow

The application is structured into modular components where data flows sequentially through validation, sorting, packing, pathfinding, and tour synthesis:

```
+-------------------------------------------------------------------------+
|                              DATA INPUT                                 |
|   locations.json (Road Network)          parcels.json (Parcel Pool)     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  STAGE 1: INTEGRITY VALIDATION                          |
|   • Discard parcels with non-positive weight or negative value          |
|   • Verify node reachability from warehouse via Dijkstra check          |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  STAGE 2: STABLE MERGE SORT                             |
|   Sort parcels by Key: (priority [1 -> 3], deadline_hours [asc])        |
|   Complexity: O(n log n) time, O(n) auxiliary space                     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             STAGE 3: 0/1 KNAPSACK DYNAMIC PROGRAMMING                   |
|   Select optimal value subset under capacity limit W = 25 kg            |
|   Construct DP Matrix [n+1][W+1] -> Backtrack to retrieve parcel IDs    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  STAGE 4: STOP AGGREGATION                              |
|   Extract distinct geographical delivery destinations from parcels      |
|   Group multiple packages destined for the same customer stop           |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             STAGE 5: DIJKSTRA'S ALL-PAIRS SHORTEST PATHS                |
|   Compute shortest paths from Warehouse & all active Stops              |
|   Generate complete Metric Distance Matrix M[a][b]                      |
|   Store predecessor dictionaries to enable turn-by-turn road recovery   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             STAGE 6: NEAREST NEIGHBOR TSP TOUR SYNTHESIS                |
|   Construct greedy tour starting and ending at Warehouse                |
|   Evaluate against Exact Permutations (Brute Force) for n <= 8          |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             STAGE 7: TURN-BY-TURN ROAD PATH EXPANSION                   |
|   Expand metric tour edges into full physical road segment sequence     |
|   Deliver outputs to Terminal UI & Interactive Canvas Web Dashboard     |
+-------------------------------------------------------------------------+
```

---

## 4. Data Representation and Mathematical Formulations

### 4.1 Parcel Schema
Each parcel $p \in P$ is represented as a 7-tuple:
$$p = (\text{id}, \text{name}, w, v, \text{prio}, d, \text{loc})$$

| Attribute | Data Type | Constraint | Semantic Role in Formulation |
|---|---|---|---|
| `id` | String | Unique | Primary identifier (e.g. `"P01"`) |
| `name` | String | Non-empty | Item descriptor (e.g. `"Laptop"`) |
| `weight` ($w$) | Integer | $w \in \mathbb{Z}^+, w \le W$ | Consumed knapsack capacity (kg) |
| `value` ($v$) | Integer | $v \in \mathbb{Z}_{\ge 0}$ | Delivery revenue in INR (objective function) |
| `priority` ($\text{prio}$) | Integer | $1 \le \text{prio} \le 3$ | Primary sorting key ($1 = \text{Urgent}, 3 = \text{Standard}$) |
| `deadline_hours` ($d$) | Integer | $d > 0$ | Secondary sorting key (time SLA left) |
| `location` ($\text{loc}$) | String | $\text{loc} \in V$ | Target delivery vertex in graph |

### 4.2 Road Network Graph Formulation
The physical delivery map is represented as an undirected weighted graph:
$$G = (V, E, w)$$
where:
- $V = \{v_1, v_2, \dots, v_{10}\}$ represents physical locations (Cyber Hub, MG Road, Sector 14, Udyog Vihar, Sohna Road, DLF Phase 3, Sushant Lok, Golf Course Road, Sector 56, and Warehouse).
- $E$ represents $15$ bidirectional physical road links.
- $w: E \to \mathbb{R}^+$ assigns non-negative travel distances in kilometers ($\text{km}$).

An **adjacency list** representation is utilized:
$$\text{graph}[u] = \{(v, w(u, v)) \mid (u, v) \in E\}$$
*Rationale*: Because the Gurugram road graph is sparse ($|E| = 15 \ll |V|^2 = 100$), adjacency lists minimize storage to $\mathcal{O}(|V| + |E|)$ and allow efficient edge traversal during Dijkstra priority relaxation.

---

## 5. Detailed Algorithmic Analysis

### 5.1 Urgency Ordering via Stable Merge Sort
- **Comparison Function**:
  $$\text{Key}(p) = (\text{priority}_p, \text{deadline\_hours}_p)$$
- **Algorithmic Mechanics**:
  Merge Sort recursively divides the list of $n$ parcels into sublists of size $n/2$ until base cases of unit length are reached. In the merge phase, elements from left and right partitions are compared. When keys are equal:
  $$\text{left}[i] \le \text{right}[j]$$
  the left element is taken first, strictly preserving initial arrival order (**stability**).
- **Asymptotic Complexity**:
  - Time: Recurrence $T(n) = 2T(n/2) + \mathcal{O}(n) \implies \mathcal{O}(n \log n)$ across best, average, and worst cases (Master Theorem Case 2).
  - Space: $\mathcal{O}(n)$ auxiliary memory for merge buffer.
- **Comparison with Alternatives**:
  - *Quick Sort*: While in-place, its worst-case time is $\mathcal{O}(n^2)$ when pivots partition poorly, and standard implementations are unstable.
  - *Bubble / Insertion Sort*: $\mathcal{O}(n^2)$ average and worst-case comparisons, completely unacceptable for large parcel backlogs.

---

### 5.2 Optimal Payload Selection via 0/1 Knapsack Dynamic Programming
- **Problem Statement**:
  Given vehicle capacity $W = 25\text{ kg}$ and $n$ sorted parcels, select a subset $S \subseteq P$ such that:
  $$\max \sum_{p \in S} v_p \quad \text{subject to} \quad \sum_{p \in S} w_p \le W$$
- **Recurrence Formulation**:
  Let $\text{table}[i][w]$ denote the optimal total value achievable using a subset of the first $i$ parcels with available capacity $w \in [0, W]$:
  $$\text{table}[i][w] = \begin{cases} 
  0 & \text{if } i = 0 \text{ or } w = 0 \\
  \text{table}[i-1][w] & \text{if } w_i > w \\
  \max\Big(\text{table}[i-1][w], \; \text{table}[i-1][w - w_i] + v_i\Big) & \text{if } w_i \le w 
  \end{cases}$$
- **Backtracking Reconstruction**:
  After populating the table matrix of dimensions $(n+1) \times (W+1)$:
  ```python
  selected = []
  w = capacity
  for i in range(n, 0, -1):
      if table[i][w] != table[i-1][w]:
          selected.append(parcels[i-1])
          w -= parcels[i-1]["weight"]
  selected.reverse()
  ```
- **Asymptotic Complexity**:
  - Time: $\mathcal{O}(n \cdot W)$ pseudo-polynomial operations.
  - Space: $\mathcal{O}(n \cdot W)$ memory to store the full DP matrix for backtracking.
- **Why Greedy Fails**:
  A greedy strategy sorting by value-to-weight density $v_i / w_i$ is optimal for the *Fractional Knapsack* problem, but fails in *0/1 Knapsack* because parcels cannot be divided. Counterexample: Capacity $W=5$, items with $(w=3, v=30)$ [ratio 10], $(w=3, v=28)$ [ratio 9.3], and $(w=5, v=50)$ [ratio 10]. Greedy selects item 1 and gets value 30, whereas the optimal subset is item 3 giving value 50.

---

### 5.3 Metric Shortest Paths via Dijkstra's Algorithm
- **Objective**:
  Determine shortest physical road distances and predecessor trees between the Warehouse and all selected delivery stops $S_{\text{stops}}$.
- **Algorithmic Mechanics**:
  Maintains a tentative distance map `dist[u]` initialized to $\infty$ (`dist[source] = 0`) and a binary min-heap storing pairs `(distance, vertex)`. At each step:
  1. Extract node $u$ with minimum tentative distance from min-heap.
  2. For each incident edge $(u, v)$ with weight $w(u, v)$, perform edge relaxation:
     $$\text{If } \text{dist}[u] + w(u, v) < \text{dist}[v]: \quad \text{dist}[v] \leftarrow \text{dist}[u] + w(u, v), \quad \text{previous}[v] \leftarrow u$$
- **Predecessor Path Recovery**:
  ```python
  def get_path(prev, start, end):
      path = []
      curr = end
      while curr is not None:
          path.append(curr)
          if curr == start: break
          curr = prev.get(curr)
      return path[::-1]
  ```
- **Asymptotic Complexity**:
  - Time: $\mathcal{O}((V + E) \log V)$ using binary min-heaps (`heapq`).
  - Space: $\mathcal{O}(V + E)$ for adjacency storage, distance dictionaries, and priority queues.
  - *Full Pipeline Cost*: Executed once for the warehouse and once for each stop ($k$ stops), resulting in $\mathcal{O}(k \cdot (V + E) \log V)$.

---

### 5.4 Tour Construction via Nearest Neighbor TSP vs. Brute-Force
- **Problem Statement**:
  Find a Hamiltonian circuit starting and ending at the Warehouse that visits all $k$ stops exactly once with minimum total distance:
  $$\min \sum_{j=1}^{k} M[\pi_j][\pi_{j+1}] \quad \text{where } \pi_0 = \pi_{k+1} = \text{Warehouse}$$
- **Nearest Neighbor Heuristic ($O(k^2)$)**:
  - From the current location, iteratively choose the unvisited destination with the smallest metric distance $M[\text{current}][\text{next}]$.
  - Return to Warehouse after visiting all stops.
  - *Pros*: Ultra-fast execution, negligible overhead.
  - *Cons*: Susceptible to greedy myopia. Can leave a distant stop for the final leg, forcing an expensive return to the warehouse.
- **Exact Brute-Force Permutations ($O(k!)$)**:
  - Generates all $(k)!$ permutations of stops, computes exact circuit distance, and selects the absolute global minimum.
  - Feasible only for small $k \le 8$ due to factorial explosion:
    - $k = 7 \implies 7! = 5,040$ iterations.
    - $k = 15 \implies 15! \approx 1.3 \times 10^{12}$ iterations (computationally prohibitive).
- **Observed Approximation Bound on NCR Map**:
  - Exact Best Route ($k=7$ stops): **$37\text{ km}$**
  - Nearest Neighbor Route: **$47\text{ km}$**
  - Approximation Difference: **$+10\text{ km}$ ($27.0\%$ error margin)**.

---

## 6. Frontend & Interactive Dashboard Design

To provide an intuitive visual demonstration for academic defense and evaluation, the project includes two distinct interfaces:

### 6.1 Interactive Web Dashboard (`web/index.html` & `server.py`)
- **Technology Stack**: Native HTML5, modern CSS3 (glassmorphism dark aesthetic), ES6 Vanilla JavaScript, Python `http.server`.
- **Key Features**:
  1. **HTML5 Canvas Map**: Renders Gurgaon road network nodes with coordinate layout, edge distances, and glow states.
  2. **Animated Route Simulation**: A dedicated delivery van (`🚚`) animates along physical road legs, with Play, Pause, Replay, and Step-by-Step controls.
  3. **Live Capacity Slider**: Real-time slider ($5\text{ kg} - 45\text{ kg}$) that dynamically triggers the Knapsack solver and updates the route graph instantly.
  4. **Deep-Dive Tab Views**:
     - *Interactive DP Table*: Displays $(n+1) \times (W+1)$ grid with green-highlighted optimal choice paths.
     - *Dijkstra Distance Matrix*: Visual heatmap grid of all-pairs distances.
     - *TSP Benchmark Card*: Live side-by-side comparison of Nearest Neighbor vs. Brute Force optimal.
- **Dual Runtime Capability**:
  - Serves via REST API `python server.py` at `http://127.0.0.1:5000/`.
  - Also operates **100% offline standalone** by opening `web/index.html` directly in any browser with embedded JS algorithm implementations!

### 6.2 Enhanced Terminal CLI (`main.py`)
- Employs ANSI color palettes, Unicode box borders (`┏━┓`, `│`, `└─┘`), and visual payload capacity meters (`[████████████████████] 25/25 kg (100%)`).
- Color-coded priority tags (`[P1-Urgent]`, `[P2-Normal]`, `[P3-Low]`).
- Clean tabular formatting for DP tables and Dijkstra matrices.

---

## 7. Comprehensive Asymptotic Complexity Analysis

Let $n$ = number of parcels, $W$ = vehicle capacity, $V$ = graph vertices (locations), $E$ = graph edges (roads), and $k$ = delivery stops ($k \le n, k \le V$).

| Algorithm | Paradigm | Time Complexity (Best) | Time Complexity (Avg) | Time Complexity (Worst) | Auxiliary Space | Practical Scalability |
|---|---|---|---|---|---|---|
| **Merge Sort** | Divide & Conquer | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Extremely scalable ($n > 10^6$) |
| **Bubble Sort** (Baseline) | Brute Force | $\Omega(n)$ (Optimized) | $\Theta(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Fails beyond $n > 5,000$ |
| **0/1 Knapsack DP** | Dynamic Programming | $\Omega(n \cdot W)$ | $\Theta(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | Scalable for integer $W \le 10^4$ |
| **Dijkstra's Algorithm** | Greedy / Priority Queue | $\Omega((V+E) \log V)$ | $\Theta((V+E) \log V)$ | $\mathcal{O}((V+E) \log V)$ | $\mathcal{O}(V + E)$ | Excellent on sparse graphs |
| **Nearest Neighbor TSP** | Greedy Heuristic | $\Omega(k^2)$ | $\Theta(k^2)$ | $\mathcal{O}(k^2)$ | $\mathcal{O}(k)$ | Fast for thousands of stops |
| **Brute-Force TSP** | Exhaustive Search | $\Omega(k!)$ | $\Theta(k!)$ | $\mathcal{O}(k!)$ | $\mathcal{O}(k)$ | Strictly restricted to $k \le 8$ |

---

## 8. Sample Execution Walkthrough and Verification

### 8.1 Input Data Configuration
- **Vehicle Payload Limit**: $25\text{ kg}$
- **Warehouse**: Central Hub at `"Warehouse"`
- **Available Parcels**: 12 parcels (IDs `P01` to `P12`)
- **Map Nodes**: 10 locations, 15 bidirectional physical roads

### 8.2 Execution Trace

#### Step 1: Input Validation
All 12 parcels validated against positive weights, positive values, and warehouse graph reachability.

#### Step 2: Merge Sort Urgency Queue
```
Rank  ID   Name             Weight   Value  Priority  Deadline  Location
1     P05  Documents          1 kg   Rs 250    P1       2 h     MG Road
2     P02  Medicines          1 kg   Rs 600    P1       3 h     Sector 14
3     P01  Laptop             3 kg   Rs 900    P1       4 h     Cyber Hub
4     P09  Mobile Phone       1 kg   Rs 800    P1       5 h     Sushant Lok
5     P08  Gift Hamper        4 kg   Rs 350    P2       8 h     Golf Course Road
6     P12  Monitor            6 kg   Rs 550    P2       9 h     Cyber Hub
7     P04  Microwave Oven    12 kg   Rs 700    P2      10 h     Sector 56
8     P07  Printer            7 kg   Rs 450    P2      12 h     Udyog Vihar
9     P03  Books Box          8 kg   Rs 300    P3      24 h     Sohna Road
10    P06  Shoes              2 kg   Rs 200    P3      30 h     DLF Phase 3
11    P11  Winter Jackets     5 kg   Rs 280    P3      36 h     Sector 14
12    P10  Water Purifier     9 kg   Rs 500    P3      48 h     Sector 56
```

#### Step 3: Knapsack Selection
- **Optimal Payload**: 8 Parcels (`P05, P02, P01, P09, P08, P12, P07, P06`)
- **Capacity Utilization**: $25 / 25\text{ kg}$ ($100\%$ full)
- **Total Revenue**: $\text{Rs } 4,100$
- **Deferred to Next Trip**: `P04, P03, P11, P10` (Totaling $34\text{ kg}$)

#### Step 4: Stop Aggregation
- 7 distinct customer delivery stops: `Cyber Hub, DLF Phase 3, Golf Course Road, MG Road, Sector 14, Sushant Lok, Udyog Vihar`.

#### Step 5: Dijkstra Shortest Paths from Warehouse
- `Warehouse -> Udyog Vihar`: $5\text{ km}$ (Direct)
- `Warehouse -> Cyber Hub`: $8\text{ km}$ (via Udyog Vihar)
- `Warehouse -> DLF Phase 3`: $9\text{ km}$ (via Udyog Vihar)
- `Warehouse -> Sector 14`: $7\text{ km}$ (Direct)
- `Warehouse -> MG Road`: $11\text{ km}$ (via Sector 14)
- `Warehouse -> Sushant Lok`: $14\text{ km}$ (via Udyog Vihar -> DLF Phase 3)
- `Warehouse -> Golf Course Road`: $16\text{ km}$ (via Sector 14 -> MG Road)

#### Step 6: TSP Route Synthesis
- **Nearest Neighbor Tour**:
  `Warehouse -> Udyog Vihar -> Cyber Hub -> DLF Phase 3 -> Sushant Lok -> MG Road -> Sector 14 -> Golf Course Road -> Warehouse`
- **Total Trip Distance**: **$47\text{ km}$**

#### Step 7: Turn-by-Turn Road Expansion
```
Warehouse -> Udyog Vihar -> Cyber Hub -> DLF Phase 3 -> Sushant Lok -> MG Road -> Sector 14 -> MG Road -> Golf Course Road -> MG Road -> Sector 14 -> Warehouse
```

---

## 9. Empirical Benchmarks and Runtime Analysis

Benchmarking experiments were conducted with a fixed random seed (`Random(42)`) using high-resolution timers (`time.perf_counter()`).

### 9.1 Experimental Benchmark Data

#### Table 9.1: Wall-Clock Runtime across Input Scales (Milliseconds)
| Algorithm | Small Input | Medium Input | Large Input | Theoretical Complexity | Empirical Fit |
|---|---|---|---|---|---|
| **Merge Sort** | $0.114\text{ ms}$ ($n=100$) | $1.600\text{ ms}$ ($n=1,000$) | $5.634\text{ ms}$ ($n=3,000$) | $\mathcal{O}(n \log n)$ | $3.5\times$ growth for $3\times n$ |
| **Bubble Sort** | $0.567\text{ ms}$ ($n=100$) | $63.298\text{ ms}$ ($n=1,000$) | $618.291\text{ ms}$ ($n=3,000$) | $\mathcal{O}(n^2)$ | $9.8\times$ growth ($3^2 \approx 9$) |
| **Knapsack DP** | $0.049\text{ ms}$ ($n=10, W=50$) | $4.533\text{ ms}$ ($n=100, W=500$) | $84.400\text{ ms}$ ($n=400, W=2,000$) | $\mathcal{O}(n \cdot W)$ | $18.6\times$ growth for $16\times (n \cdot W)$ |
| **Dijkstra** | $0.023\text{ ms}$ ($V=10$) | $0.674\text{ ms}$ ($V=500$) | $18.367\text{ ms}$ ($V=5,000$) | $\mathcal{O}((V+E) \log V)$ | Scalable across large graphs |
| **Nearest Neighbor** | $0.010\text{ ms}$ ($k=10$) | $1.519\text{ ms}$ ($k=200$) | $42.838\text{ ms}$ ($k=1,000$) | $\mathcal{O}(k^2)$ | $28.2\times$ growth for $5\times k$ ($5^2 = 25$) |

#### Table 9.2: Nearest Neighbor vs. Brute-Force Factorial Scaling
| Stops ($k$) | Nearest Neighbor (ms) | Brute Force (ms) | Permutations Evaluated | NN Error Margin (%) |
|---|---|---|---|---|
| **5** | $0.004\text{ ms}$ | $0.035\text{ ms}$ | $24$ | $19.4\%$ |
| **6** | $0.004\text{ ms}$ | $0.110\text{ ms}$ | $120$ | $0.0\%$ (Optimal) |
| **7** | $0.005\text{ ms}$ | $0.700\text{ ms}$ | $720$ | $0.0\%$ (Optimal) |
| **8** | $0.005\text{ ms}$ | $4.934\text{ ms}$ | $5,040$ | $0.0\%$ (Optimal) |
| **9** | $0.007\text{ ms}$ | $43.901\text{ ms}$ | $40,320$ | $0.0\%$ (Optimal) |

*Key Observation*: While Brute Force runtime explodes by over $1,250\times$ from $k=5$ to $k=9$ ($0.035\text{ ms} \to 43.901\text{ ms}$), Nearest Neighbor remains practically flat ($0.004\text{ ms} \to 0.007\text{ ms}$).

### 9.2 Graphical Visualizations
The benchmark plots generated by the suite are included below:

- **Sorting Comparison**: `report/charts/sorting.png` (demonstrates diverging curves of $n \log n$ vs $n^2$).
- **Knapsack DP Growth**: `report/charts/knapsack.png` (linear with matrix cell area $n \times W$).
- **Dijkstra Graph Scaling**: `report/charts/dijkstra.png` (efficient heap relaxation up to $5,000$ vertices).
- **TSP Greedy vs. Factorial**: `report/charts/tsp_exact_vs_nn.png` (demonstrates exponential/factorial explosion of permutations).
- **Comprehensive Benchmark**: `report/charts/all_algorithms.png`.

---

## 10. Limitations, Bottlenecks, and Future Scope

### 10.1 Identified Limitations
1. **Deadline Decoupling in TSP**: Nearest Neighbor optimizes purely for distance, not time SLA. In the sample run, parcel `P05` has a 2-hour deadline but is visited 5th due to spatial sequencing.
2. **Single-Vehicle Trip Model**: Parcels exceeding $25\text{ kg}$ are simply queued for a subsequent dispatch run rather than optimizing multi-vehicle fleets.
3. **Integral Weight Discretization**: Knapsack DP requires whole-number integer weights ($1\text{ kg}, 2\text{ kg}$). Fractional or high-precision floating weights would inflate table dimension $W$.

### 10.2 Recommended Algorithmic Enhancements
- **2-Opt Local Search**: Post-process the Nearest Neighbor tour by iteratively swapping edge pairs $(u, v)$ and $(x, y)$ to eliminate path crossings, reducing the $27\%$ gap to $<5\%$.
- **Vehicle Routing Problem with Time Windows (VRPTW)**: Incorporate penalties for deadline violations into the tour objective function.
- **Space-Optimized Knapsack**: If traceback of parcel IDs is not required, space can be reduced from $\mathcal{O}(n \cdot W)$ to $\mathcal{O}(W)$ using a 1D rolling array.

---

## 11. Viva Voce Technical Preparation

This section provides comprehensive answers to anticipated theoretical and practical questions during the project defense:

**Q1: Why did you choose Merge Sort over Quick Sort or Heap Sort?**  
*Answer*: Merge Sort guarantees $\mathcal{O}(n \log n)$ time in all cases (worst, average, and best). Unlike standard Quick Sort which can degrade to $\mathcal{O}(n^2)$ when pivots partition poorly, Merge Sort never degrades. Furthermore, Merge Sort is **stable**: parcels with identical priority and deadline preserve their original input ordering, ensuring fair FIFO handling.

**Q2: Why is Dynamic Programming necessary for parcel packing instead of a Greedy approach?**  
*Answer*: The parcel problem is a discrete **0/1 Knapsack problem** where parcels cannot be broken into fractions. A greedy approach based on value-to-weight ratio $v/w$ can leave empty capacity that could have been filled by a higher-value combination of slightly heavier items. Dynamic programming explores all overlapping subproblems via optimal substructure, guaranteeing the true global maximum value.

**Q3: Can Dijkstra handle negative road weights? Why does your implementation check for this?**  
*Answer*: No. Dijkstra's algorithm relies on the greedy property that once a vertex is extracted from the priority queue, its shortest distance is finalized. A negative edge weight can invalidate this assumption and lead to incorrect shortest paths or infinite cycling. The data validation step enforces $w(u, v) \ge 0$. If negative edge weights were present, the Bellman-Ford algorithm ($\mathcal{O}(V \cdot E)$) would be required.

**Q4: Explain why Nearest Neighbor found a 47 km route while the brute-force route was 37 km.**  
*Answer*: Nearest Neighbor is a greedy heuristic that makes locally optimal choices at each step without lookahead. At Sector 14, it chose Golf Course Road simply because it was the closest unvisited stop, but this forced a very long return journey back to the warehouse across the entire map ($16\text{ km}$). The brute-force method evaluates all $k!$ complete circuits globally, avoiding costly closing edges.

**Q5: What makes Knapsack DP "pseudo-polynomial"?**  
*Answer*: Its running time is $\mathcal{O}(n \cdot W)$. While linear in the numeric value of $W$, in computational complexity theory the input size is measured by the number of bits required to represent $W$, which is $\log_2 W$. Therefore, the time complexity is exponential in the length of the input representation ($\mathcal{O}(n \cdot 2^b)$ where $b = \text{bits of } W$).

---

## 12. Conclusion

The **Mini-Courier Dispatch Planner & Route Optimization Engine** successfully synthesizes four classic algorithmic paradigms—**Divide and Conquer (Merge Sort)**, **Dynamic Programming (0/1 Knapsack)**, **Single-Source Shortest Paths (Dijkstra)**, and **Heuristic Search (Nearest Neighbor TSP)**—into an integrated urban logistics decision support tool.

Both theoretical asymptotic claims and empirical profiling results demonstrate that the pipeline is highly efficient, processing realistic city delivery runs in under $10\text{ milliseconds}$. The inclusion of an interactive web dashboard with animated road graph simulation bridges the gap between abstract algorithmic concepts and tangible software engineering.

---

## 13. References & Execution Guidelines

### Academic References:
1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
2. Kleinberg, J., & Tardos, É. (2006). *Algorithm Design*. Pearson Education.
3. Applegate, D. L., Bixby, R. E., Chvátal, V., & Cook, W. J. (2006). *The Traveling Salesperson Problem: A Computational Study*. Princeton University Press.

### Execution Instructions:
```bash
# Navigate to project directory
cd c:\Users\anura\OneDrive\Desktop\DAA\Mini-Courier-Planner

# Run Enhanced Terminal Planner
python main.py
python main.py --capacity 15

# Launch Interactive Web Dashboard Server
python server.py
# (Open http://127.0.0.1:5000/ in any modern web browser)
# Or simply double-click web/index.html to run directly offline!

# Run Automated Performance Benchmarks
python performance/benchmark.py
```
