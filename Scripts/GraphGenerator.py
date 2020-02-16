import random
import networkx as nx
import matplotlib.pyplot as plt

class GraphGenerator:

    def __init__(self,max_nodes,max_edges):
        self.max_nodes = max_nodes
        self.max_edges = max_edges


    def generate_weighted_graph(self,w_range=(0,100),seed=random.randint(0,1000),verbose=True):
        n_nodes = self.max_nodes
        m_edges = self.max_edges
        p = 2 * m_edges / (n_nodes * (n_nodes - 1))
        if verbose:
            print('Maximum Edges',n_nodes * (n_nodes - 1) / 2)
            print('Probability to make an edge',p)
        G = nx.generators.fast_gnp_random_graph(n_nodes, p, seed=seed)
        for (u,v,w) in G.edges(data=True):
            w['weight'] = random.randint(w_range[0],w_range[1])
        if verbose:
            print('Edges',len(G.edges))
            print('Connectivity',nx.is_connected(G))
        self.G = G
        return G


    def generate_graph(self,seed=random.randint(0,1000),verbose=True):
        n_nodes = self.max_nodes
        m_edges = self.max_edges
        p = 2 * m_edges / (n_nodes * (n_nodes - 1))
        if verbose:
            print('Maximum Edges',n_nodes * (n_nodes - 1) / 2)
            print('Probability to make an edge',p)
        G = nx.generators.fast_gnp_random_graph(n_nodes, p, seed=seed)
        if verbose:
            print('Edges',len(G.edges))
            print('Connectivity',nx.is_connected(G))
        self.G = G
        return G


    def draw_grapgh(self,G=None,figsize=(8,3)):
        if not G:
            try:
                G = self.G
            except:
                print('ERROR: Graph G does not exist. \nSpeify arg G or call generate_graph methods')
                return
        plt.figure(figsize=(figsize[0],figsize[1]))
        pos = nx.spring_layout(G)
        nx.draw(G,pos)
        nx.draw_networkx_labels(G,pos,font_color='white',font_weight='bold')
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        plt.draw()
        plt.show()
        return
