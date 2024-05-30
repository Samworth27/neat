class Neuron:
    text = "N"

    def __init__(self, id: int, rank: int) -> None:
        self.id = id
        self.rank: int = rank

    def __str__(self) -> str:
        return f"{self.text}{self.id}-R{self.rank}"

    def __repr__(self) -> str:
        return str(self)


class InputNeuron(Neuron):
    text = "I"

    def __init__(self, id) -> None:
        super().__init__(id=id, rank=0)


class BiasNeuron(InputNeuron):
    text = "B"

    def __init__(self, id: int) -> None:
        super().__init__(id=id)


class SensorNeuron(InputNeuron):
    text = "S"

    def __init__(self, id) -> None:
        super().__init__(id)


class HiddenNeuron(Neuron):
    text = "H"

    def __init__(self, id: int) -> None:
        super().__init__(id, 1)


class OutputNeuron(Neuron):
    text = "O"

    def __init__(self, id: int) -> None:
        super().__init__(id=id, rank=1)
