from neat.network._synapse import Synapse
from neat.network._neuron import Neuron, InputNeuron


class Network:
    def __init__(self):
        self.neurons = set()
        self.synapses = set()

    def add_neuron(self, neuron: Neuron) -> None:
        self.neurons.add(neuron)

    def add_synapse(self, synapse: Synapse) -> None:
        self.synapses.add(synapse)
        self.neurons.update(set([synapse.target, synapse.source]))


if __name__ == "__main__":
    n0 = InputNeuron(0)
    n1 = InputNeuron(1)
    n2 = InputNeuron(2)
    s0 = Synapse(0, n0, n1, 1, True)
    s1 = Synapse(1, n0, n2, 1, True)

    net = Network()
    net.add_synapse(s0)
    net.add_synapse(s1)
    print(net.synapses)
    print(net.neurons)