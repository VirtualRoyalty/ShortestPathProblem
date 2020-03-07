import sys
sys.path.append('../')

from Scripts import GraphGenerator as gg
from Algorithms import JohnsonSP as jsp
from Algorithms import FloydSP as fsp
#from importlib import reload  # Python 3.4+ only.
from datetime import datetime as time
import progressbar

class StressTest: 
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.error_counter = 0
        self.error_graphs = []
        self.all_ahortest_path = {}
        self.working_time = 0
        self.G = {}

    def run(self, number_of_iterations, max_nodes, max_edges):
        start_time = time.now()
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for i in range(number_of_iterations):
            bar.update(i)
            generator = gg.GraphGenerator(max_nodes, max_edges)
            self.G = generator.generate_weighted_graph(verbose = False)
            johnson_algorithm = jsp.JohnsonSP(self.G)
            
            floyd_algorithm = fsp.FloydSP(self.G)
            pred, floyd_dist = floyd_algorithm.floyd_predecessor_and_distance()
            floyd_shortest_paths = floyd_algorithm.get_path_from_predcessor(pred)
            johnsons_shortest_paths = johnson_algorithm.get_path_by_dijkstra()
            
            # if path dicts are not equal, then find collisions
            # and check path len node by node
            if floyd_shortest_paths != johnsons_shortest_paths:
                if not self.is_equal_path_length(\
                        floyd_dist, floyd_shortest_paths, johnsons_shortest_paths):
                    self.error_graphs.append(self.G)
                    self.error_counter += 1

            self.working_time = time.now() - start_time

        if self.verbose:
            self.print_statistic()
        return self.error_graphs
            
    def is_equal_path_length(self, floyd_dist, floyd_shortest_paths, johnson_shortest_paths):
        # find collision
        for i in range(len(self.G)):
            for j in range(len(self.G)):
                if floyd_shortest_paths[i][j] != johnson_shortest_paths[i][j]:
                    floyd_path_length, johnson_path_lenght = \
                    self.get_path_lengths(floyd_shortest_paths[i][j], floyd_dist, johnson_shortest_paths[i][j])
                    return floyd_path_length == johnson_path_lenght
                    
    def get_path_lengths(self, floyd_shortest_path, dist_floyd, johnson_shortest_path):
        # go through path lists and accumulate weights of edges
        floyd_path_length, johnson_path_lenght = 0, 0
        for i in range(0, len(floyd_shortest_path) - 1):
            floyd_path_length += dist_floyd[floyd_shortest_path[i]][floyd_shortest_path[i + 1]]
        for i in range(0, len(johnson_shortest_path) - 1):
            johnson_path_lenght += self.G[johnson_shortest_path[i]][johnson_shortest_path[i + 1]]['weight']
        return floyd_path_length, johnson_path_lenght

    def print_statistic(self):
        print("Working time: {}, errors: {}".format(self.working_time, self.error_counter))
