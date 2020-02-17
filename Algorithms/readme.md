## Floyd all shortest path algorithm

```
from Algorithms import FloydSP as fsp
floyd = fsp.FloydSP(G)
pred,dist = floyd.floyd_predecessor_and_distance()
floyd.get_path_from_predcessor(pred)
```
