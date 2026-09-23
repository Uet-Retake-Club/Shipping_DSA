# Smart Delivery Network Design Using Minimum Spanning Tree (MST)

This project implements the Minimum Spanning Tree (MST) problem to optimize logistics delivery networks. It uses **Kruskal's algorithm** with a **Disjoint Set Union (DSU)** data structure to efficiently connect hubs, warehouses, and delivery points with minimum total edge weight.

## 📂 Project Structure

```
Shipping_DSA/
├── data/                   # Generated datasets (JSON, GraphML) and visualizations
├── src/
│   ├── algorithms/         # MST algorithms implementation
│   │   ├── dsu.py          # Disjoint Set Union with path compression & union by rank
│   │   ├── kruskal.py      # Kruskal's MST implementation (O(E log E))
│   │   └── prim.py         # (Optional) Prim's algorithm implementation
│   ├── core/               # Core graph data structures
│   │   ├── graph.py        # Graph, Node, Edge classes
│   │   └── graphml_handler.py  # GraphML export/import utility
│   └── generators/         # Dataset generation modules
│       ├── dataset_generator.py  # Create small, clustered, and benchmark datasets
│       ├── spatial_utils.py      # Geographic distance calculations
│       └── validator.py          # Data validation and analysis
├── tests/
│   ├── test_dsu.py         # DSU unit tests
│   ├── test_kruskal.py     # MST algorithm tests
│   └── test_generators.py  # Dataset generation tests
├── scripts/
│   ├── run_benchmark.py    # Run all algorithms on benchmarks
│   ├── visualize.py        # Generate network visualizations
│   ├── analyze.py          # Network analysis and metrics
│   └── compare.py          # Compare Kruskal vs Prim
├── .gitignore              # Files to ignore in version control
├── README.md               # Project overview and documentation
└── requirements.txt        # Python dependencies
```

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Shipping_DSA
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Algorithms

The project implements two MST algorithms in `src/algorithms/`:

### 1. Kruskal's Algorithm (Primary)

**Implementation**: `src/algorithms/kruskal.py`

**Time Complexity**: O(E log E) or O(E log V)

**Space Complexity**: O(V + E)

**Key Features**:
- Uses Disjoint Set Union (DSU) to detect cycles
- Supports disconnected graphs (produces MST forest)
- Deterministic tie-breaking for edge weights
- Early exit optimization when V-1 edges are found

### 2. Prim's Algorithm (Optional)

**Implementation**: `src/algorithms/prim.py`

**Time Complexity**: O(E + V log V) using min-heap

**Space Complexity**: O(V + E)

**Key Features**:
- Builds MST from a single starting node
- Growing tree structure
- Handles disconnected graphs gracefully

## 📈 Data Generation

The `src/generators/` module creates various dataset types:

### 1. Small Network (10 nodes)
```python
from src.generators import create_small_network

g = create_small_network()
# Output: data/networks/metro_logistics_small_10.graphml
```

### 2. Clustered Network
Creates geographically realistic networks with clusters:
```python
from src.generators import generate_clustered_network

g = generate_clustered_network(
    num_nodes=100,
    num_clusters=5,
    k_neighbors=4,
    random_seed=42,
    disconnected=False
)
```

### 3. Benchmark Datasets
Generates three standard sizes for performance testing:
```python
from src.generators import generate_benchmark_datasets

generate_benchmark_datasets(small=10, medium=50, large=500)
# Output: data/networks/benchmark_small_10.graphml
#         data/networks/benchmark_medium_50.graphml
#         data/networks/benchmark_large_500.graphml
```

## 🛠️ Usage Examples

### Run Kruskal's Algorithm
```python
from src.algorithms import kruskal_mst

result = kruskal_mst(graph)

# Get MST edges
for edge in result.mst_edges:
    print(f"{edge.u} --({edge.weight})--> {edge.v}")

# Get statistics
print(f"Total cost: {result.total_cost}")
print(f"Edges in MST: {result.num_edges_in_mst}")
print(f"Execution time: {result.execution_time_ms} ms")
```

### Generate Visualizations
```bash
# Small network visualization
python scripts/visualize.py --network data/networks/metro_logistics_small_10.graphml --output visualizations/small_network.png

# Benchmark visualizations
python scripts/visualize.py --network data/networks/benchmark_medium_50.graphml --output visualizations/medium_network.png
```

### Run Benchmark Tests
```bash
python scripts/run_benchmark.py --output data/results/benchmark_results.json
```

### Compare Algorithms
```bash
python scripts/compare.py --network data/networks/benchmark_large_500.graphml --output data/results/comparison.json
```

## 📋 Test Coverage

### Unit Tests
```bash
# Test DSU implementation
python -m tests.test_dsu

# Test Kruskal's algorithm
python -m tests.test_kruskal

# Test dataset generation
python -m tests.test_generators
```

### Test Results Format
Test results are saved to `tests/results.xml` using pytest-html plugin:
```xml
<testsuite name="pytest" errors="0" skipped="0" tests="6" failures="0" time="0.544">
    <testcase classname="tests.test_dsu.DSU Tests" name="test_union_by_rank" time="0.048" />
    ...
</testsuite>
```

## 📝 Performance Benchmarks

### Benchmark Results (Example)

**Kruskal's Algorithm Performance**

| Dataset | Nodes | Edges | MST Cost | Time (ms) | Edges Considered | Connected |
|---------|-------|-------|----------|-----------|------------------|-----------|
| Small   | 10    | 14    | 366.41   | 0.2047    | 7                | True      |
| Medium  | 50    | 95    | 549.02   | 0.6013    | 24               | True      |
| Large   | 500   | 479   | 3325.99  | 46.7228   | 249              | True      |

### Time Complexity Analysis

| Algorithm | Initialization | Sorting Edges | DSU Operations | Total Time | Notes |
|-----------|----------------|---------------|----------------|------------|-------|
| Kruskal   | O(V)           | O(E log E)    | O(E α(V))      | O(E log E) | Optimal for sparse graphs |
| Prim      | O(V)           | O(1)          | O(E log V)     | O(E log V) | Better for dense graphs |

## 🎨 Network Analysis

The `scripts/analyze.py` script generates comprehensive metrics:

```python
from src.generators import generate_benchmark_datasets
from scripts import analyze_network

generate_benchmark_datasets()
results = analyze_network("data/networks/benchmark_large_500.graphml")

# Print statistics
print(f"Number of nodes: {results['num_nodes']}")
print(f
    
