from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from music_graph.datamodel.graph.node import GraphNode


@dataclass()
class Graph:
    nodes: Dict[str, GraphNode]
    edges: List[Tuple[str, str, Optional[float], Optional[float]]]
