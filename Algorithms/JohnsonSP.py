from networkx.algorithms.shortest_paths.weighted import _bellman_ford, _dijkstra, _weight_function
from networkx.algorithms.shortest_paths import astar
import networkx as nx

class JohnsonSP:

    def __init__(self, G, weight='weight'):
        if not nx.is_weighted(G, weight=weight):
            raise nx.NetworkXError('Graph is not weighted.')

        self.G = G
        self.dist = {v: 0 for v in G}
        self.pred = {v: [] for v in G}
        self.weight = _weight_function(G, weight)
        # Calculate distance of shortest paths
        self.dist_bellman = _bellman_ford(G, list(G), self.weight, pred=self.pred, dist=self.dist)

    # Update the weight function to take into account the Bellman--Ford
    # relaxation distances.
    def new_weight(self, u, v, d):
        return self.weight(u, v, d) + self.dist_bellman[u] - self.dist_bellman[v]

    def dist_path_by_dijkstra(self, v):
        paths = {v: [v]}
        _dijkstra(self.G, v, self.new_weight, paths=paths)
        return paths

    def dist_path_by_astar(self, v):
        return {u_i: astar.astar_path(self.G, v, u_i) for u_i in self.G}

    def get_path_by_dijkstra(self):
        return {v: self.dist_path_by_dijkstra(v) for v in self.G}

    def get_path_by_astar(self):
        return {v: self.dist_path_by_astar(v) for v in self.G}
