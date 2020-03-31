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
            self.astar_path(self.G, v, u_i, heuristic, paths=paths)

    def get_path_by_dijkstra(self):
        return {v: self.dist_path_by_dijkstra(v) for v in self.G}

    def get_path_by_astar(self, heuristic=None):
        paths = np.empty((len(self.G), len(self.G)), dtype=list)
        for v in self.G:
            self.dist_path_by_astar(v, heuristic, paths=paths)
        # print(paths)
        return
        
    def astar_path(self, G, source, target, heuristic=None, weight='weight', paths=None):
        
        if paths[target][source] != None:
            return
        
        if G.is_multigraph():
            raise NetworkXError("astar_path() not implemented for Multi(Di)Graphs")

        if heuristic is None:
            # The default heuristic is h=0 - same as Dijkstra's algorithm
            def heuristic(G, u, v):
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
                paths[source][target] = path
                #print(paths[target][source], paths[source][target])
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
    
    def _dijkstra(self, G, source, get_weight, pred=None, paths=None, cutoff=None,
              target=None, heuristic=None):

        if heuristic is None:
            # The default heuristic is h=0 - same as Dijkstra's algorithm
            def heuristic(G, u, v):
                return 0
        
        G_succ = G.succ if G.is_directed() else G.adj

        push = heappush
        pop = heappop
        dist = {}  # dictionary of final distances
        seen = {source: 0}
        c = count()
        fringe = []  # use heapq with (distance,label) tuples
        push(fringe, (0, next(c), source))
        while fringe:
            (d, _, v) = pop(fringe)
            if v in dist:
                continue  # already searched this node.
            dist[v] = d
            if v == target:
                break

            for u, e in G_succ[v].items():
                cost = get_weight(v, u, e)
                if cost is None:
                    continue
                vu_dist = dist[v] + get_weight(v, u, e)
                if cutoff is not None:
                    if vu_dist > cutoff:
                        continue
                if u in dist:
                    if vu_dist < dist[u]:
                        raise ValueError('Contradictory paths found:',
                                         'negative weights?')
                elif u not in seen or vu_dist < seen[u]:
                    seen[u] = vu_dist
                    push(fringe, (vu_dist, next(c), u))
                    if paths is not None:
                        paths[u] = paths[v] + [u]
                    if pred is not None:
                        pred[u] = [v]
                elif vu_dist == seen[u]:
                    if pred is not None:
                        pred[u].append(v)

        if paths is not None:
            return (dist, paths)
        if pred is not None:
            return (pred, dist)
        return dist
