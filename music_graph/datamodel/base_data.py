from typing import Protocol, runtime_checkable


@runtime_checkable
class BaseData(Protocol):
    @property
    def data_id(self) -> str:
        ...
