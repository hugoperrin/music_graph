from dataclasses import dataclass
from typing import Dict, List, Optional

from music_graph.datamodel.base_data import BaseData


@dataclass()
class NeighborData:
    id: str
    edge_weight: Optional[float] = None
    edge_cap: Optional[float] = None


@dataclass()
class GraphNode:
    id: str
    object: Optional[BaseData]
    neighbor_ids: List[NeighborData]
    value: Optional[float] = None

    def to_node_dict(self, add_object_data: bool = False) -> Dict:
        base_data: Dict = {"id": self.id, "value": self.value}
        if add_object_data and self.object is not None:
            base_data.update(self.object.to_dict())
        return base_data

    @staticmethod
    def from_dict(dict_data: Dict) -> "GraphNode":
        return GraphNode(
            id=dict_data["id"], value=dict_data["value"], neighbor_ids=[], object=None,
        )
