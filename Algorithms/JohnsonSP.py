from networkx.algorithms.shortest_paths.weighted import _bellman_ford, _dijkstra, _weight_function
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

    def dist_path(self, v):
        paths = {v: [v]}
        _dijkstra(self.G, v, self.new_weight, paths=paths)
        return paths

    def get_path(self):
        return {v: self.dist_path(v) for v in self.G}
