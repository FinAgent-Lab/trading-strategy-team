from abc import ABC, abstractmethod


class BaseNode(ABC):

    def __call__(self, *args: any, **kwds: any) -> any:
        return self.invoke(*args, **kwds)

    @abstractmethod
    def invoke(self) -> any: ...
