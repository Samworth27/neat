class Gene():
    def __init__(self) -> None:
        raise NotImplementedError

    def clone(self) -> "Gene":
        raise NotImplementedError

class NeuronGene(Gene):
    text = "U"
    accept_incoming = False
    accept_outgoing = False

    def __init__(self, id=None):
        self.id = id

    def __repr__(self) -> str:
        return f"[{self.text}{self.id}]"

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
        self.innovation_id: int

    def clone(self) -> "SynapseGene":
        return SynapseGene(
            self.source_node, self.target_node, self.weight, self.enabled
        )

    @property
    def key(self):
        return (self.source_node, self.target_node)

    def set_innovation_id(self, id):
        self.innovation_id = id

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        # return f"[{self.source_node:02}{gene_active_symbol if self.enabled else gene_inactive_symbol}{self.target_node:02}]"
        _value = round(self.weight, 1) if self.enabled else "   "
        return f"[{self.source_node:02}'-{_value}-'{self.target_node:02}]"
