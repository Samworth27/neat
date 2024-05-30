from neat.genome import Genome
from neat.genome.gene import Gene, InputNeuronGene, SensorNeuronGene, SynapseGene, BiasNeuronGene, OutputNeuronGene, HiddenNeuronGene
from neat.network import Network
from neat.network.draw import draw_network

if __name__ == "__main__":

    genome = Genome()
    genome.add_gene(BiasNeuronGene())  # 0
    genome.add_gene(SensorNeuronGene())  # 1
    genome.add_gene(SensorNeuronGene())  # 2
    genome.add_gene(OutputNeuronGene())  # 3
    genome.add_gene(OutputNeuronGene())  # 4
    genome.add_gene(HiddenNeuronGene())  # 5
    genome.add_gene(HiddenNeuronGene())  # 6
    genome.add_gene(HiddenNeuronGene())  # 7
    genome.add_gene(SynapseGene(0, 5, 1, True))
    genome.add_gene(SynapseGene(1, 5, 1, True))
    genome.add_gene(SynapseGene(5, 6, 1, True))
    genome.add_gene(SynapseGene(2, 6, 1, True))
    genome.add_gene(SynapseGene(6, 3, 1, True))
    genome.add_gene(SynapseGene(1, 7, 1, True))
    genome.add_gene(SynapseGene(7, 4, 1, True))
    test = Network.from_genome(genome)

    genome_2 = Genome()
    genome_2.add_gene(BiasNeuronGene())  # 0
    genome_2.add_gene(SensorNeuronGene())  # 1
    genome_2.add_gene(SensorNeuronGene())  # 2
    genome_2.add_gene(OutputNeuronGene())  # 3
    genome_2.add_gene(OutputNeuronGene())  # 4
    genome_2.add_gene(HiddenNeuronGene())  # 5
    genome_2.add_gene(HiddenNeuronGene())  # 6
    genome_2.add_gene(SynapseGene(1, 5, 2, True))
    genome_2.add_gene(SynapseGene(5, 6, 2, True))
    genome_2.add_gene(SynapseGene(0, 6, 2, True))
    genome_2.add_gene(SynapseGene(2, 5, 2, True))
    genome_2.add_gene(SynapseGene(6, 3, 2, True))

    test2 = Network.from_genome(genome_2)

    

    draw_network(test, "network 1")
    # draw_network(test2, "network 2")
    # child = test.crossover(test2)
    test.mutate()
