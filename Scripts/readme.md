# How to use GraphGenerator sample

``` 
from Scripts import GraphGenerator as gg
n_nodes = 10
m_edges = 14
generator = gg.GraphGenerator(max_nodes=n_nodes,max_edges=m_edges)
G = generator.generate_weighted_graph()
generator.draw_grapgh()
```

# How to run stress tests

``` 
st = reload(st)

stress_tests = st.StressTest(verbose = True)
error_graphs = stress_tests.run(number_of_iterations = 100, max_nodes = 10, max_edges = 20)
```
Stress test steps:
- generation connectivity graph with specified number edges and nodes;
- run Floyd and Johnson algorithm
- check returned lists of shortest paths
- checking lenght for not equal shortest path lists
- return list of graphs with errors, if there are any
