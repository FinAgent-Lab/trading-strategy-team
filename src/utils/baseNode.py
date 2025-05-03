from abc import ABC, abstractmethod


class BaseNode(ABC):

    async def __call__(self, *args: any, **kwds: any) -> any:
        return await self.invoke(*args, **kwds)

    @abstractmethod
    def invoke(self) -> any: ...
