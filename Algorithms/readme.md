## Floyd all shortest path algorithm

```
from Algorithms import FloydSP as fsp
floyd = fsp.FloydSP(G)
pred,dist = floyd.floyd_predecessor_and_distance()
floyd.get_path_from_predcessor(pred)
```
## Johnson all shortest path algorithm

```
from Algorithms import JohnsonSP as jsp
import networkx as nx
from importlib import reload  # Python 3.4+ only.

#jsp = reload(jsp)            # if local changes

johnson = jsp.JohnsonSP(G)
```
## Johnson all shortest path algorithm by Dijkstra
```
j_paths = johnson.get_path_by_dijkstra()
```
## Johnson all shortest path algorithm by Astar (A*)
```
a_star_paths = johnson.get_path_by_astar()
```
## Default networkX Johnson algoritm checking
```
nx_j_paths = nx.johnson(G)
```
## Seidel algorithm implementation (http://math.mit.edu/~rothvoss/18.304.1PM/Presentations/2-Chandler-slideslect2.pdf)
```
from Algorithms import SeidelSP as ssp
# ssp = reload(ssp)             # if local changes
seidel = ssp.SeidelSP()
seidel.get_distance_matrix(A)
```