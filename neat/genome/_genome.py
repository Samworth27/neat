from collections.abc import Iterable, Iterator
from typing import TypeVar, Union
from neat.util import SparseList, random_bool

from .gene import Gene, NeuronGene, SynapseGene, OutputNeuronGene

AnyGene = Union[NeuronGene, SynapseGene]

class Genome:

    innovations: dict[tuple, int] = {}

    def __init__(self) -> None:
        self.neuron_genes: SparseList[NeuronGene] = SparseList()
        self.synapse_genes: SparseList[SynapseGene] = SparseList()

    @classmethod
    def get_innovation_id(cls, key):
        if key not in cls.innovations:
            cls.innovations[key] = len(cls.innovations)
            print(f"New innovation found {key}")

        return cls.innovations[key]

    def clone(self) -> "Genome":
        new_genome = type(self)()
        for gene in self:
            new_genome.add_gene(gene.clone())
        return new_genome

    @classmethod
    def _random_genes(cls, parent_1: "Genome", parent_2: "Genome") -> list[AnyGene]:
        gene_list: list[AnyGene|None] = []
        for i in cls.innovations.values():
            inherited_genome = parent_1 if random_bool() else parent_2
            inherited_gene = inherited_genome.synapse_genes[i]
            if inherited_gene:
                inherited_gene = inherited_gene.clone()
                source_gene = inherited_genome.neuron_genes[inherited_gene.source_node]
                target_gene = inherited_genome.neuron_genes[inherited_gene.target_node]
                gene_list = [*gene_list, inherited_gene, source_gene, target_gene]
        for gene in parent_1.neuron_genes:
            if (
                isinstance(gene, (NeuronGene, OutputNeuronGene))
                and gene not in gene_list
            ):
                gene_list.append(gene)
        print("GL:", gene_list)
        return [g for g in gene_list if g is not None]

    @classmethod
    def _favoured_genes(
        cls, dominate_genome: "Genome", recessive_genome: "Genome"
    ) -> list[Gene]:
        gene_list: list[Gene] = list(dominate_genome.neuron_genes.iter_skip_nones())
        for i in cls.innovations.values():
            dom_gene = dominate_genome.synapse_genes[i]
            rec_gene = recessive_genome.synapse_genes[i]

            if dom_gene and not rec_gene:
                gene_list.append(dom_gene)
            if dom_gene and rec_gene:
                gene_list.append(dom_gene if random_bool() else rec_gene)
        return gene_list

    @classmethod
    def _select_genes(
        cls, parent_1: "Genome", parent_2: "Genome", favoured_parent: int | None
    ):

        if not favoured_parent:
            return cls._random_genes(parent_1, parent_2)

        if favoured_parent == 1:
            return cls._favoured_genes(parent_1, parent_2)
        else:
            return cls._favoured_genes(parent_2, parent_1)

    @classmethod
    def crossover(
        cls,
        dominate_genome: "Genome",
        recessive_genome: "Genome",
        equal_inheritance: bool = False,
    ):
        new_genome = Genome()
        new_genome.add_genes(
            cls._select_genes(
                dominate_genome, recessive_genome, None if equal_inheritance else 1
            )
        )
        return new_genome

    def add_gene(self, gene: Gene):
        if not isinstance(gene, Gene):
            raise TypeError("Must be type: Gene")
        if isinstance(gene, NeuronGene):
            if gene.id is None:
                gene.id = len(self.neuron_genes)
            if gene.id not in self.neuron_genes:
                self.neuron_genes[gene.id] = gene
        if isinstance(gene, SynapseGene):
            gene.set_innovation_id(self.get_innovation_id(gene.key))
            self.synapse_genes[gene.innovation_id] = gene

    def add_genes(self, genes: Iterable[Gene]):
        for gene in genes:
            self.add_gene(gene)

    def __iter__(self) -> Iterator[Gene]:
        return iter([*self.neuron_genes, *self.synapse_genes])
