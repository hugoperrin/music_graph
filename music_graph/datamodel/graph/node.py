from dataclasses import dataclass
from typing import List, Optional

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
