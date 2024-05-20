from enum import Enum
from typing import Iterable, Iterator
from util import random_bool, SparseList


class NodeType(Enum):
    BIAS = "B"
    INPUT = "I"
    OUTPUT = "O"
    HIDDEN = "H"


class Gene:
    pass


class Genome(Iterable):
    def __init__(self):
        self.genes:list[Gene] = SparseList()

    def add_gene(self, position, gene: Gene):
        if not position:
            position = len(self.genes)
        self.genes[position] = gene
        
    def __iter__(self)->Iterator[Gene]:
        yield from self.genes


class NodeGene(Gene):
    def __init__(self, id, node_type: NodeType):
        self.id = id
        self.node_type: NodeType = node_type
        
    def clone(self):
        return NodeGene(self.id, self.node_type)

    def __repr__(self) -> str:
        return f"[{str(self.node_type.value)}]"

    def __str__(self) -> str:
        return self.__repr__()


class NodeGenome(Genome):
    def __init__(
        self,
        num_input_nodes: int,
        num_output_nodes: int,
        num_hidden_nodes,
        bias_node: bool,
    ):
        super().__init__()
        if bias_node:
            self.add_gene(NodeType.BIAS)

        for node_type, count in [
            (NodeType.INPUT, num_input_nodes),
            (NodeType.OUTPUT, num_output_nodes),
            (NodeType.HIDDEN, num_hidden_nodes),
        ]:
            for _ in range(count):
                self.add_gene(node_type)

    @property
    def length(self):
        return len(self.genes)

    def add_gene(self, node_type: NodeType):
        super().add_gene(None, NodeGene(self.length, node_type))
        
    def __iter__(self)->Iterator[NodeGene]:
        yield from self.genes

    def __str__(self) -> str:
        return "".join([str(gene) for gene in self.genes])


class EdgeGene(Gene):
    def __init__(self, source_node, target_node, weight: float, enabled: bool):
        self.source_node = source_node
        self.target_node = target_node
        self.weight: float = weight
        self.enabled: bool = enabled
        self.innovation_id: int = None
        
    def clone(self):
        return EdgeGene(self.source_node, self.target_node, self.weight, self.enabled)

    @property
    def key(self):
        return (self.source_node, self.target_node)

    def set_innovation_id(self, id):
        self.innovation_id = id

    def __str__(self) -> str:
        gene_active_symbol = "---" #"⚪"
        gene_inactive_symbol = "-x-" #"⚫"
        # return f"[{self.source_node:02}{gene_active_symbol if self.enabled else gene_inactive_symbol}{self.target_node:02}]"
        return f"[{self.source_node:02}{f'-{round(self.weight,1)if self.enabled else '   '}-' }{self.target_node:02}]"


class EdgeGenome(Genome):
    innovations = dict()

    @classmethod
    def get_innovation_id(cls, key):
        if key not in cls.innovations:
            cls.innovations[key] = len(cls.innovations)

        return cls.innovations[key]

    def __init__(self):
        super().__init__()
        
    def __iter__(self) -> Iterator[EdgeGene]:
        yield from [(i, self.genes[i]) for i in range(len(self.innovations))]

    def add_gene(self, gene: EdgeGene):
        gene.set_innovation_id(self.get_innovation_id(gene.key))
        self.genes[gene.innovation_id] = gene
        
    def crossover(self, partner_genome):
        print(self)
        print(partner_genome)
        child_genome = EdgeGenome()
        for i in range(len(self.innovations)):
            if self.genes[i]:
                if partner_genome.genes[i]:
                    if random_bool():
                        #inherit from this genome
                        child_genome.add_gene(self.genes[i].clone())
                    else:
                        child_genome.add_gene(partner_genome.genes[i].clone())
                else:
                    child_genome.add_gene(self.genes[i].clone())
        return child_genome
    
    def mutate(self):
        mutated_genome = EdgeGenome()
        
        def mutate_node(self):
            pass
        
        def mutate_connections(self):
            pass
        
        def mutate_weight(self):
            pass
        
        for gene in self.genes:
            print(gene)
                    
            

    def __str__(self) -> str:
        if not len(self.innovations):
            return "{}"
        return "{" + "".join(f"{gene if gene else "[  -   -  ]"}" for id, gene in self) + "}"


if __name__ == "__main__":
    test = EdgeGenome()
    test.add_gene(EdgeGene(0,4,0.8,True))
    test.add_gene(EdgeGene(1,4,0.3,True))
    test.add_gene(EdgeGene(2,5,0.7,True))
    test.mutate()
