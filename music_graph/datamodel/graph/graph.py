from dataclasses import dataclass
from typing import Dict, Hashable, List, Tuple

import networkx as nx

from music_graph.datamodel.graph.node import GraphNode


@dataclass()
class MusicGraph:
    graph: nx.Graph
    node_aliases: Dict[Hashable, List[Hashable]]
    raw_node: Dict[Hashable, GraphNode]

    def add_node(self, node: GraphNode):
        node_id: str = self.resolve_id(node)
        data_tuple: Tuple = (node_id, node.to_node_dict())
        self.graph.add_node(data_tuple)

    def resolve_id(self, node: GraphNode) -> str:
        # TODO: do the resolving process to avoid duplicates between sources
        return node.id
