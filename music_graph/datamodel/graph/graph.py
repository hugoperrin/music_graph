from dataclasses import dataclass, field
from typing import Dict, Hashable, List, Tuple

import networkx as nx

from music_graph.datamodel.graph.node import GraphNode


@dataclass()
class MusicGraph:
    graph: nx.Graph = nx.Graph()
    node_aliases: Dict[Hashable, List[Hashable]] = field(default_factory=dict)
    raw_node: Dict[Hashable, GraphNode] = field(default_factory=dict)

    def add_node(self, node: GraphNode):
        node_id: str = self.resolve_id(node)
        data_tuple: Tuple = (node_id, node.to_node_dict())
        self.graph.add_node(data_tuple)

    def resolve_id(self, node: GraphNode) -> str:
        # TODO: do the resolving process to avoid duplicates between sources
        return node.id

    def write(self, path: str) -> None:
        # TODO: do the serialization and writing to a file here
        ...

    @staticmethod
    def read(path: str):
        # TODO: do the reading and deserialization here
        return None
