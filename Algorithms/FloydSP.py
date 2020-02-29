import copy
import networkx as nx
from collections import defaultdict


class FloydSP:


    def __init__(self,G):
        self.dist = defaultdict(lambda : defaultdict(lambda: float('inf')))
        for u in G:
            self.dist[u][u] = 0
        self.pred = defaultdict(dict)
        self.undirected = not G.is_directed()
        self.G = G


    def floyd_predecessor_and_distance(self):
        G = self.G
        dist = self.dist
        pred = self.pred
        for u,v,d in G.edges(data=True):
            e_weight = d.get('weight', 1.0)
            dist[u][v] = min(e_weight, dist[u][v])
            pred[u][v] = u
            if self.undirected:
                dist[v][u] = min(e_weight, dist[v][u])
                pred[v][u] = v
        for w in G:
            for u in G:
                for v in G:
                    if dist[u][v] > dist[u][w] + dist[w][v]:
                        dist[u][v] = dist[u][w] + dist[w][v]
                        pred[u][v] = pred[w][v]
        return dict(pred), dict(dist)

    def get_path_from_predcessor(self,predecessors):
        all_shortest_path = {}
        shortest_path_dct = {}
        for source in self.G:
            for target in self.G:
                if source == target:
                    shortest_path_dct[source] = [target]
                    continue
                prev = predecessors[source]
                curr = prev[target]
                path = [target, curr]
                while curr != source:
                    curr = prev[curr]
                    path.append(curr)
                shortest_path_dct[target] = list(reversed(path))
            all_shortest_path[source] = copy.copy(shortest_path_dct)
        return all_shortest_path
