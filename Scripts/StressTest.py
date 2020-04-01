import sys
sys.path.append('../')

from Scripts import GraphGenerator as gg
from Algorithms import JohnsonSP as jsp
from Algorithms import FloydSP as fsp
from Algorithms import SeidelSP as ssp
from importlib import reload  # Python 3.4+ only.
from datetime import datetime as time
import networkx as nx
import numpy as np
import random
import progressbar

class StressTest: 
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.error_counter = 0
        self.error_graphs = []
        self.all_ahortest_path = {}
        self.working_time = {
            'seidel' : [],
            'johnson': [],
            'floyd'  : [],
        }
        self.G = {}

    def dist_to_array(self, dist):
        N = len(dist)
        shortest_path_array = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                shortest_path_array[i][j] = dist[i][j]
        return shortest_path_array
        
    def run_seidel_floyd_test(self, number_of_iterations, max_nodes, max_edges):
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for i in range(number_of_iterations):
            bar.update(i)
            generator = gg.GraphGenerator(max_nodes=max_nodes,max_edges=max_edges)
            self.G = generator.generate_weighted_graph(w_range=(1,1), verbose = self.verbose)
            A = np.array(nx.to_numpy_array(self.G))
            
            floyd = fsp.FloydSP(self.G)
            start_time = time.now()
            _,floyd_dist = floyd.floyd_predecessor_and_distance()
            self.working_time['floyd'].append(time.now() - start_time)
            
            seidel = ssp.SeidelSP()
            start_time = time.now()
            seidel_sp = seidel.get_distance_matrix(A)
            self.working_time['seidel'].append(time.now() - start_time)
            
            if not np.array_equal(self.dist_to_array(floyd_dist), seidel_sp):
                self.error_graphs.append(self.G)
                self.error_counter += 1
                if self.verbose:
                    print("not equal distance matrix")
            else:
                if self.verbose:
                    print("equal distance matrix")
        return {'error_graphs' : self.error_graphs, 'seidel' : np.mean(self.working_time['seidel']), 'floyd'  : np.mean(self.working_time['floyd'])}
        
    def run_johnsons_floyd_test(self, number_of_iterations, max_nodes, max_edges, heuristic=None):
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for i in range(number_of_iterations):
            bar.update(i)
            generator = gg.GraphGenerator(max_nodes, max_edges)
            if heuristic:
                self.G = generator.generate_weighted_graph(w_range=(1,1), verbose = self.verbose)
            else:
                self.G = generator.generate_pseudo_real_graph(w_range=(1,1), verbose = self.verbose)

            johnson_algorithm = jsp.JohnsonSP(self.G)
            floyd_algorithm = fsp.FloydSP(self.G)

            start_time = time.now()
            pred, floyd_dist = floyd_algorithm.floyd_predecessor_and_distance()
            self.working_time['floyd'].append(time.now() - start_time)

            floyd_shortest_paths = floyd_algorithm.get_path_from_predcessor(pred)
            
            start_time = time.now()
            if heuristic:
                johnsons_shortest_paths = johnson_algorithm.get_path_by_astar(heuristic)
            else:
                johnsons_shortest_paths = johnson_algorithm.get_path_by_dijkstra()
            self.working_time['johnson'].append(time.now() - start_time)
                
            # if path dicts are not equal, then find collisions
            # and check path len node by node
            if floyd_shortest_paths != johnsons_shortest_paths:
                if not self.is_equal_path_length(\
                        floyd_dist, floyd_shortest_paths, johnsons_shortest_paths):
                    self.error_graphs.append(self.G)
                    self.error_counter += 1
        if self.verbose:
            self.print_statistic()
        return {'error_graphs' : self.error_graphs, 
                'johnson' : np.mean(self.working_time['johnson']), 
                'floyd'  : np.mean(self.working_time['floyd'])}
    
#    def get_G_coord(self, min_coord=0, max_coord=100):
#        for i in range(len(self.G)):
#            self.G.nodes[i]['coord'] = (random.randint(min_coord, max_coord), \
#                                   random.randint(min_coord, max_coord))
    @staticmethod
    def get_path_lengths(G, floyd_shortest_path, dist_floyd, johnson_shortest_path, verbose=False):
        # go through path lists and accumulate weights of edges
        floyd_path_length, johnson_path_lenght = 0, 0
        for i in range(0, len(floyd_shortest_path) - 1):
            floyd_path_length += dist_floyd[floyd_shortest_path[i]][floyd_shortest_path[i + 1]]
        for i in range(0, len(johnson_shortest_path) - 1):
            johnson_path_lenght += G[johnson_shortest_path[i]][johnson_shortest_path[i + 1]]['weight']
        if verbose:
            print("floyd: {} \njohnson: {}\n len: {} {} \n".format(floyd_shortest_path, johnson_shortest_path, floyd_path_length, johnson_path_lenght, ))
        return round(floyd_path_length, 1), round(johnson_path_lenght, 1)

    def is_equal_path_length(self, floyd_dist, floyd_shortest_paths, johnson_shortest_paths):
        # find collision
        for i in range(len(self.G)):
            for j in range(len(self.G)):
                if floyd_shortest_paths[i][j] != johnson_shortest_paths[i][j]:
                    # print(floyd_shortest_paths[i][j], johnson_shortest_paths[i][j])

                    floyd_path_length, johnson_path_lenght = \
                    self.get_path_lengths(self.G, floyd_shortest_paths[i][j], floyd_dist, johnson_shortest_paths[i][j])
                    # print("lens:", floyd_path_length, johnson_path_lenght)
                    return floyd_path_length == johnson_path_lenght

    def print_statistic(self):
        print("Working time: {}, errors: {}".format(self.working_time, self.error_counter))
