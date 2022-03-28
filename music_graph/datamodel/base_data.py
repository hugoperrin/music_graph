from typing import Dict, Protocol, runtime_checkable


@runtime_checkable
class BaseData(Protocol):
    @property
    def data_id(self) -> str:
        ...

    def to_dict(self) -> Dict:
        ...
