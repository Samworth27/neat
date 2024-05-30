from random import choice
from neat.genome import Genome
from neat.genome.gene import SynapseGene, NeuronGene, InputNeuronGene

# class Mutate:
#     def mutate_add_node(self:'Network', num_attempts:int = 5):
#         for attempt in range(num_attempts):
#             new_source = choice(self.neurons)
#             new_target = choice(self.neurons)
#             if new_source == new_target:
#                 continue
#             if issubclass(new_source.type, type(Gene.Neuron.Output)):
#                 continue
#             if issubclass(new_target.type, type(Gene.Neuron.Input)):
#                 continue
#             print(new_source, "->", new_target)
#             break


class Neuron:
    def __init__(self, id) -> None:
        self.id = id
        self.incoming: set[Synapse]
        self.outgoing: set[Synapse]
        self.rank: int
        self.type: type

    @classmethod
    def from_gene(cls, gene: NeuronGene):
        new_instance = cls(gene.id)
        new_instance.type = type(gene)
        if issubclass(new_instance.type, InputNeuronGene):
            new_instance.rank = 0
        if gene.accept_incoming:
            new_instance.incoming = set()
            new_instance.rank = 1
        if gene.accept_outgoing:
            new_instance.outgoing = set()
        return new_instance

    def update_rank(self, source: "Neuron"):
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
    def from_gene(cls, gene: SynapseGene, network: "Network"):
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
    def __init__(self) -> None:
        self.genome = Genome()
        self.neurons: dict[int, Neuron] = {}
        self.synapses: dict[int, Synapse] = {}

    @classmethod
    def from_genome(cls, genome: Genome):
        new_instance = cls()
        new_instance.genome = genome
        new_instance._process_genome()
        return new_instance

    def crossover(self, recessive_network: "Network") -> "Network":

        child_genome = Genome.crossover(self.genome, recessive_network.genome, True)
        child_network = Network.from_genome(child_genome)

        return child_network

    # def mutate(self)->None:
    #     self.mutate_add_node()

    def _process_genome(self) -> None:
        for gene in self.genome.neuron_genes:
            self.add_neuron(Neuron.from_gene(gene))

        for gene in self.genome.synapse_genes.iter_skip_nones():
            print(gene)
            self.add_synapse(Synapse.from_gene(gene, self))

    def add_neuron(self, neuron: Neuron):
        self.neurons[neuron.id] = neuron

    def add_synapse(self, synapse: Synapse):
        self.synapses[synapse.innovation_id] = synapse

