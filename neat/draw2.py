from graphviz import Digraph
from typing import TYPE_CHECKING
from genes2 import Gene

if TYPE_CHECKING:
    from network2 import Network


def draw_network(network: "Network"):
    graph = Digraph(directory="graphs", format="png", engine="dot")

    with (
        graph.subgraph(name="inputs") as c_i,
        graph.subgraph(name="outputs") as c_o,
    ):
        c_i.attr(rank="same", ordering="out")
        c_o.attr(rank="same")
        for node in network.neurons.values():
            name = str(node.id)
            label = str(node)
            match node.type:
                case  Gene.Neuron.Input.Bias | Gene.Neuron.Input.Sensor:
                    c_i.node(name,label)
                    if node.id > 0:
                        c_i.edge(
                            tail_name=str(node.id - 1),
                            head_name=str(node.id),
                            style="invis",
                        )
                case Gene.Neuron.Output:
                    c_o.node(name,label)
                
                case Gene.Neuron.Hidden:
                    graph.node(name,label)

                

    for edge in network.genome.synapse_genes:
        graph.edge(str(edge.source_node), str(edge.target_node))

    graph.view()


# graph = Graph(directory='graphs', format='png',
#           graph_attr=dict(ranksep='2', rankdir='LR', color='white', splines='line'),
#           node_attr=dict(label='', shape='circle', width='0.1'),
#           edge_attr=dict(constraint='false'))

# def draw_cluster(name, length):
#     with graph.subgraph(name=f'cluster_{name}') as c:
#         c.attr(label=name, rank='same')
#         for i in range(length):
#             c.node(f'{name}_{i}')

# draw_cluster('input', 10)
# draw_cluster('output', 4)

# source_active = [0, 1, 2, 3]
# sink_active = [2, 3]

# for i_input in source_active:
#     for i_output in sink_active:
#         graph.edge(f'input_{i_input}', f'output_{i_output}')

# def central_neurons(layer_size: int):
#     if layer_size % 2 == 1:
#         return {layer_size // 2}
#     else:
#         return {layer_size // 2, layer_size // 2 - 1}

# for source_id in central_neurons(layer_size=10):
#     for sink_id in central_neurons(layer_size=4):
#         graph.edge(f'input_{source_id}', f'output_{sink_id}',
#                 constraint='true', style='invis')
# graph.view()
