# How to use GraphGenerator sample

``` 
from Scripts import GraphGenerator as gg
n_nodes = 10
m_edges = 14
generator = gg.GraphGenerator(max_nodes=n_nodes,max_edges=m_edges)
G = generator.generate_weighted_graph()
generator.draw_grapgh()
