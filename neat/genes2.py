from enum import Enum
from typing import Iterable, Iterator
from util import random_bool, SparseList


class Gene:
    pass


class NeuronGene(Gene):
    text = "U"
    accept_incoming = False
    accept_outgoing = False

    def __init__(self):
        self.id = None

    def clone(self):
        return NeuronGene(self.id, self.node_type)

    def __repr__(self) -> str:
        return f"[{self.text}]"

    def __str__(self) -> str:
        return self.__repr__()


class InputNeuronGene(NeuronGene):
    text = "I"
    accept_outgoing = True


class BiasNeuronGene(InputNeuronGene):
    text = "B"


class SensorNeuronGene(InputNeuronGene):
    text = "S"


class HiddenNeuronGene(NeuronGene):
    text = "H"
    accept_outgoing = True
    accept_incoming = True


class OutputNeuronGene(NeuronGene):
    text = "O"
    accept_incoming = True


class SynapseGene(Gene):
    def __init__(
        self, source_node: int, target_node: int, weight: float, enabled: bool
    ):
        self.source_node = source_node
        self.target_node = target_node
        self.weight: float = weight
        self.enabled: bool = enabled
        self.innovation_id: int = None

    def clone(self):
        return SynapseGene(
            self.source_node, self.target_node, self.weight, self.enabled
        )

    @property
    def key(self):
        return (self.source_node, self.target_node)

    def set_innovation_id(self, id):
        self.innovation_id = id

    def __str__(self) -> str:
        gene_active_symbol = "---"  # "⚪"
        gene_inactive_symbol = "-x-"  # "⚫"
        # return f"[{self.source_node:02}{gene_active_symbol if self.enabled else gene_inactive_symbol}{self.target_node:02}]"
        return f"[{self.source_node:02}{f'-{round(self.weight,1)if self.enabled else '   '}-' }{self.target_node:02}]"


InputNeuronGene.Bias = BiasNeuronGene
InputNeuronGene.Sensor = SensorNeuronGene

NeuronGene.Input = InputNeuronGene
NeuronGene.Hidden = HiddenNeuronGene
NeuronGene.Output = OutputNeuronGene

Gene.Neuron = NeuronGene
Gene.Synapse = SynapseGene

class Genome:

    innovations = dict()

    @classmethod
    def get_innovation_id(cls, key):
        if key not in cls.innovations:
            cls.innovations[key] = len(cls.innovations)

        return cls.innovations[key]

    def __init__(self):
        self.neuron_genes: list[NeuronGene] = list()
        self.synapse_genes: SparseList[SynapseGene] = SparseList()

    def add_gene(self, gene: Gene):
        if not isinstance(gene, Gene):
            raise TypeError("Must be type: Gene")
        if isinstance(gene, NeuronGene):
            gene.id = len(self.neuron_genes)
            self.neuron_genes.append(gene)
        if isinstance(gene, SynapseGene):
            gene.set_innovation_id(self.get_innovation_id(gene.key))
            self.synapse_genes[gene.innovation_id] = gene
