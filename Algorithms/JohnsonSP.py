from networkx.algorithms.shortest_paths.weighted import _bellman_ford, _dijkstra, _weight_function
from networkx.algorithms.shortest_paths import astar
from heapq import heappush, heappop
from itertools import count
from networkx import NetworkXError
import networkx as nx
import numpy as np
import copy

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

    def dist_path_by_astar(self, v, heuristic=None, paths=None):
        for u_i in self.G:
            self.astar_path(self.G, v, u_i, heuristic)

    def get_path_by_dijkstra(self):
        return {v: self.dist_path_by_dijkstra(v) for v in self.G}

    def get_path_by_astar(self, heuristic=None):
        return {v: self.dist_path_by_astar(v, heuristic) for v in self.G}

    def astar_path(self, G, source, target, heuristic=None, weight='weight'):

        if G.is_multigraph():
            raise NetworkXError("astar_path() not implemented for Multi(Di)Graphs")

        if heuristic is None:
            # The default heuristic is h=0 - same as Dijkstra's algorithm
            def heuristic(_, u, v):
                return 0

        push = heappush
        pop = heappop

        # The queue stores priority, node, cost to reach, and parent.
        # Uses Python heapq to keep in priority order.
        # Add a counter to the queue to prevent the underlying heap from
        # attempting to compare the nodes themselves. The hash breaks ties in the
        # priority and is guarenteed unique for all nodes in the graph.
        c = count()
        queue = [(0, next(c), source, 0, None)]

        # Maps enqueued nodes to distance of discovered paths and the
        # computed heuristics to target. We avoid computing the heuristics
        # more than once and inserting the node into the queue too many times.
        enqueued = {}
        # Maps explored nodes to parent closest to the source.
        explored = {}

        while queue:
            # Pop the smallest item from queue.
            _, __, curnode, dist, parent = pop(queue)

            if curnode == target:
                path = [curnode]
                node = parent
                while node is not None:
                    path.append(node)
                    node = explored[node]
                path.reverse()
                return path

            if curnode in explored:
                continue

            explored[curnode] = parent

            for neighbor, w in G[curnode].items():
                if neighbor in explored:
                    continue
                ncost = dist + w.get(weight, 1)
                if neighbor in enqueued:
                    qcost, h = enqueued[neighbor]
                    # if qcost < ncost, a longer path to neighbor remains
                    # enqueued. Removing it would need to filter the whole
                    # queue, it's better just to leave it there and ignore
                    # it when we visit the node a second time.
                    if qcost <= ncost:
                        continue
                else:
                    h = heuristic(self.G, neighbor, target)
                enqueued[neighbor] = ncost, h
                push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

        raise nx.NetworkXNoPath("Node %s not reachable from %s" % (source, target))
