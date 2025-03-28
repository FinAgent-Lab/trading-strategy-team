from abc import ABC, abstractmethod
from typing_extensions import Self


class GraphBuilder(ABC):

    @abstractmethod
    def build(self) -> Self: ...

    @abstractmethod
    def get_nodes(self) -> dict[str, any]: ...

    @abstractmethod
    def get_edges(self) -> list[tuple[str, str]]: ...

    @abstractmethod
    def invoke(self, input: dict[str, any]): ...
