from genes import NodeGene, NodeGenome, NodeType, EdgeGene, EdgeGenome


class Neuron:
    def __init__(self, id, node_type: NodeType, level=0):
        self.id = id
        self.node_type = node_type
        self.level = level
        self.outgoing: list[Synapse] = []

    def add_outgoing(self, synapse: "Synapse"):
        self.outgoing.append(synapse)
        self.update_levels()

    def update_levels(self):
        for synapse in self.outgoing:
            if synapse.target.level == self.level:
                synapse.target.level = self.level + 1
                synapse.target.update_levels()
            if synapse.target.level < self.level:
                synapse.target.level = self.level
                synapse.target.update_levels()

    def __repr__(self):
        return f"Neuron({self.node_type}| level {self.level})"


class Synapse:
    def __init__(self, source: Neuron, target: Neuron, weight, enabled):
        self.source = source
        self.target = target
        self.weight = weight
        self.enabled = enabled

        source.add_outgoing(self)

    def __repr__(self):
        return f"Synapse({self.source.id}->{self.target.id} | w:{self.weight}, e:{self.enabled})"


def create_test_genomes():
    node_genome = NodeGenome(2, 1, 4, True)
    edge_genome = EdgeGenome()
    edge_genome.add_gene(EdgeGene(4, 5, 0.5, True))
    edge_genome.add_gene(EdgeGene(5, 6, 0.5, True))
    edge_genome.add_gene(EdgeGene(4, 6, 0.5, True))
    edge_genome.add_gene(EdgeGene(0, 4, 0.5, True))
    edge_genome.add_gene(EdgeGene(6, 3, 0.5, True))
    return node_genome, edge_genome


class Network:
    def __init__(self, node_genome: NodeGenome, edge_genome: EdgeGenome):
        self.inputs: list[Neuron] = list()
        self.outputs: list[Neuron] = list()
        self.hidden: list[Neuron] = list()
        self.neurons: dict[int, Neuron] = dict()
        self.synapses: list[Synapse] = list()
        for gene in node_genome:
            neuron = Neuron(gene.id, gene.node_type, 0)
            self.neurons[gene.id] = neuron
            if gene.node_type in [NodeType.BIAS, NodeType.INPUT]:
                self.inputs.append(neuron)
            if gene.node_type == NodeType.OUTPUT:
                neuron.level = 1
                self.outputs.append(neuron)
            if gene.node_type == NodeType.HIDDEN:
                neuron.level = 1
                self.hidden.append(neuron)

        for _, gene in edge_genome:
            synapse = Synapse(
                self.neurons[gene.source_node],
                self.neurons[gene.target_node],
                gene.weight,
                gene.enabled,
            )
            self.synapses.append(synapse)

        output_level = max([n.level for n in self.hidden]) + 1
        for n in self.outputs:
            n.level = output_level


if __name__ == "__main__":
    test_network = Network(*create_test_genomes())
    print(test_network.neurons)
    print(test_network.synapses)
