from typing import TYPE_CHECKING

from neat.genome.gene import SensorNeuronGene, BiasNeuronGene, OutputNeuronGene, InputNeuronGene, HiddenNeuronGene
from graphviz import Digraph #type: ignore

if TYPE_CHECKING:
    from neat.network import Network


def draw_network(network: "Network", title: str):
    graph = Digraph(name=title, directory="graphs", format="png", engine="dot")
    graph.attr("graph",rankdir="LR")
    with (
        graph.subgraph(name="inputs") as c_i,
        graph.subgraph(name="outputs") as c_o,
    ):
        c_i.attr(rank="same", ordering="out")
        c_o.attr(rank="same")

        prev_input_node_id = None
        prev_output_node_id = None

        for node in network.neurons.values():
            name = str(node.id)
            label = str(node)
            match node.type:
                case InputNeuronGene():
                    c_i.node(name, label)
                    if prev_input_node_id:
                        c_i.edge(
                            tail_name=str(prev_input_node_id),
                            head_name=str(node.id),
                            style="invis",
                        )
                    prev_input_node_id = node.id

                case OutputNeuronGene():
                    c_o.node(name, label)
                    if prev_output_node_id:
                        c_o.edge(
                            tail_name=str(prev_output_node_id),
                            head_name=str(node.id),
                            style="invis"
                        )
                    prev_output_node_id = node.id

                case HiddenNeuronGene():
                    graph.node(name, label)

    for edge in network.genome.synapse_genes.iter_skip_nones():
        graph.edge(str(edge.source_node), str(edge.target_node), label=str(edge.weight))

    graph.view()