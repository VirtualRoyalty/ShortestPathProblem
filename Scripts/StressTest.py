import sys
sys.path.append('../')

from Scripts import GraphGenerator as gg
from Algorithms import JohnsonSP as jsp
from Algorithms import FloydSP as fsp
#from importlib import reload  # Python 3.4+ only.
from datetime import datetime as time

class StressTest: 
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.error_counter = 0
        self.error_graphs = []
        self.all_ahortest_path = {}
        self.working_time = 0
        
    def run(self, number_of_iterations, max_nodes, max_edges):
        start_time = time.now()
        for i in range(number_of_iterations):
            generator = gg.GraphGenerator(max_nodes, max_edges)
            G = generator.generate_weighted_graph(verbose = False)
            
            johnson_algorithm = jsp.JohnsonSP(G)
            
            floyd_algorithm = fsp.FloydSP(G)
            pred,dist = floyd_algorithm.floyd_predecessor_and_distance()
            
            if floyd_algorithm.get_path_from_predcessor(pred) != johnson_algorithm.get_path_by_dijkstra():
                self.error_counter+=1
                self.error_graphs.append(G)
        self.working_time = time.now() - start_time
        if self.verbose:
            self.print_statistic()
        return self.error_graphs
            
    def print_statistic(self):
        print("Working time: {}, errors: {}".format(self.working_time, self.error_counter))
