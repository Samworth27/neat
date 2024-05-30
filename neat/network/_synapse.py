from typing import TYPE_CHECKING, Any

from ._neuron import Neuron

if TYPE_CHECKING:
    from ._neuron import Neuron


class Synapse:
    _FROZEN = False
    frozen_attributes:list[str] = ["innovation_id", "source", "target"]

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
        self._FROZEN = True

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.frozen_attributes and self._FROZEN:
            raise RuntimeError
        super().__setattr__(name, value)

    @property
    def key(self) -> tuple[int, int]:
        return (self.source.id, self.target.id)

    def __hash__(self) -> int:
        return hash(self.key)
