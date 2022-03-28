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
    object: BaseData
    neighbor_ids: List[NeighborData]
    value: Optional[float] = None

    def to_node_dict(self, add_object_data: bool = False) -> Dict:
        base_data: Dict = {"id": self.id, "value": self.value}
        if add_object_data:
            base_data.update(self.object.to_dict())
        return base_data
