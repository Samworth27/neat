from genes2 import Genome, Gene


class Neuron:
    def __init__(self, id):
        self.id = id
        self.incoming: set['Synapse'] = None
        self.outgoing: set['Synapse'] = None
        self.rank:int = 0
        self.type:Gene.Neuron = Gene.Neuron

    @classmethod
    def from_gene(cls, gene: Gene.Neuron):
        new_instance = cls(gene.id)
        new_instance.type = type(gene)
        if gene.accept_incoming:
            new_instance.incoming = set()
            new_instance.rank = 1
        if gene.accept_outgoing:
            new_instance.outgoing = set()
        return new_instance
    
    def update_rank(self, source:'Neuron'):
        if self.rank <= source.rank:
            self.rank = source.rank + 1
            if self.outgoing:
                for synapse in self.outgoing:
                    synapse.target.update_rank(self)
    
    def __str__(self):
        return f"{self.type.text}{self.id}-R{self.rank}"

class Synapse:
    def __init__(
        self,
        innovation_id: int,
        source: Neuron,
        target: Neuron,
        weight: float,
        enabled: bool,
    ):
        self.innovation_id = innovation_id
        self.source: Neuron = source
        self.target: Neuron = target
        self.weight: float = weight
        self.enabled: bool = enabled

    @classmethod
    def from_gene(cls, gene: Gene.Synapse, network: "Network"):
        source: Neuron = network.neurons[gene.source_node]
        target: Neuron = network.neurons[gene.target_node]
        new_instance = cls(
            gene.innovation_id, source, target, gene.weight, gene.enabled
        )
        source.outgoing.add(new_instance)
        target.incoming.add(new_instance)
        target.update_rank(source)
        return new_instance
    



class Network:
    def __init__(self):
        self.genome = genome
        self.neurons:dict[int,Neuron] = dict()
        self.synapses:dict[int,Synapse] = dict()

    @classmethod
    def from_genome(cls, genome: Genome):
        new_instance = cls()
        new_instance.genome = genome
        new_instance._process_genome()
        return new_instance

    def _process_genome(self):
        for gene in self.genome.neuron_genes:
            self.add_neuron(Neuron.from_gene(gene))
        for gene in self.genome.synapse_genes:
            self.add_synapse(Synapse.from_gene(gene, self))

    def add_neuron(self, neuron: Neuron):
        self.neurons[neuron.id] = neuron

    def add_synapse(self, synapse: Synapse):
        self.synapses[synapse.innovation_id] = synapse


if __name__ == "__main__":
    from draw2 import draw_network
    genome = Genome()
    genome.add_gene(Gene.Neuron.Input.Bias())
    genome.add_gene(Gene.Neuron.Input.Sensor())
    genome.add_gene(Gene.Neuron.Input.Sensor())
    genome.add_gene(Gene.Neuron.Output())
    genome.add_gene(Gene.Neuron.Hidden())
    genome.add_gene(Gene.Neuron.Hidden())
    genome.add_gene(Gene.Neuron.Hidden())
    genome.add_gene(Gene.Neuron.Output())
    genome.add_gene(Gene.Synapse(0, 4, 0.5, True))
    genome.add_gene(Gene.Synapse(1, 4, 0.5, True))
    genome.add_gene(Gene.Synapse(2, 5, 0.5, True))
    genome.add_gene(Gene.Synapse(5, 4, 0.5, True))
    genome.add_gene(Gene.Synapse(4, 3, 0.5, True))
    genome.add_gene(Gene.Synapse(0,6, 0.5, True))
    genome.add_gene(Gene.Synapse(6, 3, 0.5, True))
    genome.add_gene(Gene.Synapse(6, 7, 0.5, True))
    test = Network.from_genome(genome)
    draw_network(test)
