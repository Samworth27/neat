import networkx as nx
import matplotlib.pyplot as plt
from network import create_test_genomes, Network, NodeType

if __name__ == "__main__":
    network = Network(*create_test_genomes())
    
    nodes = dict()
    levels = dict()
    for node in network.neurons.values():
        if node.level not in levels:
            levels[node.level] = dict()
        
        levels[node.level][node.id] = node
    
    G= nx.Graph()
    for i, layer in levels.items():
        for j, node in layer.items():
            nodes[j] = node
            G.add_node(node, layer=i, label = j)
            
    for e in network.synapses:
        G.add_edge(e.source, e.target)
        
    plt.figure(figsize=(8,8))
    pos = nx.multipartite_layout(G, subset_key="layer")
    colours = {
        NodeType.BIAS: "blue",
        NodeType.INPUT: "yellow",
        NodeType.HIDDEN: "red",
        NodeType.OUTPUT: "green"
    }
    color = [colours[n.node_type] for n in G.nodes]
    nx.draw(G,pos,node_color = color)
    plt.show()
        
    #     for edge in network.synapses:
    #         brush = viznet.EdgeBrush('-')
    #         e = brush >> (nodes[edge.source.id], nodes[edge.target.id])