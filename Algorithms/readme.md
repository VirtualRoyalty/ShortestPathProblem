## Floyd all shortest path algorithm

```
from Algorithms import FloydSP as fsp
Floyd = fsp.FloydSP(G)
pred,dist = Floyd.floyd_predecessor_and_distance()
floyd.get_path_from_predcessor(pred)
```
## Johnson all shortest path algorithm

```
from Algorithms import JohnsonSP as jsp
import networkx as nx
from importlib import reload  # Python 3.4+ only.

#jsp = reload(jsp)            # if local changes

johnson = jsp.JohnsonSP(G)
j_paths = johnson.get_path()
nx_j_paths = nx.johnson(G)
```
