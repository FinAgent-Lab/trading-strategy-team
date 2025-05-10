from abc import ABC, abstractmethod


class BaseNode(ABC):

    async def __call__(self, *args: any, **kwargs: any) -> any:
        return await self.invoke(*args, **kwargs)

    @abstractmethod
    def invoke(self) -> any: ...
