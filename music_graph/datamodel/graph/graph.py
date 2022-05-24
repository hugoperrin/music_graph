import json
from dataclasses import dataclass, field
from typing import Dict, Hashable, List, Tuple

import networkx as nx

from music_graph.datamodel.graph.node import GraphNode


@dataclass()
class MusicGraph:
    graph: nx.Graph = nx.Graph()
    node_aliases: Dict[Hashable, List[Hashable]] = field(default_factory=dict)
    raw_node: Dict[Hashable, GraphNode] = field(default_factory=dict)

    def add_node(self, node: GraphNode) -> str:
        data_tuple: Tuple = (node.id, node.to_node_dict())
        self.graph.add_node(data_tuple)
        if node.id not in self.node_aliases:
            self.node_aliases[node.id] = [node.id]
        if node.id not in self.raw_node:
            self.raw_node[node.id] = node
        return node.id

    def add_edge(self, source: str, target: str, **kwargs) -> bool:
        self.graph.add_edge(source, target, **kwargs)
        return True

    def resolve_id(self, node: GraphNode) -> str:
        # TODO: do the resolving process to avoid duplicates between sources
        return node.id

    def write(self, path: str) -> None:
        nx.write_adjlist(self.graph, MusicGraph.networkx_path(path=path))
        with open(MusicGraph.alias_path(path=path), "w") as f:
            json.dump(self.node_aliases, f)
        with open(MusicGraph.nodes_path(path=path), "w") as f:
            json_data: Dict[Hashable, Dict] = {}
            for _id, node in self.raw_node.items():
                json_data[_id] = node.to_node_dict()
            json.dump(json_data, f)

    @staticmethod
    def networkx_path(path: str) -> str:
        return f"{path}.graph"

    @staticmethod
    def alias_path(path: str) -> str:
        return f"{path}.aliases"

    @staticmethod
    def nodes_path(path: str) -> str:
        return f"{path}.nodes"

    @staticmethod
    def read(path: str):
        graph: nx.Graph = nx.read_adjlist(MusicGraph.networkx_path(path=path))
        with open(MusicGraph.alias_path(path=path), "r") as f:
            aliases: Dict[Hashable, List[Hashable]] = json.load(f)
        with open(MusicGraph.nodes_path(path=path), "r") as f:
            nodes: Dict[Hashable, Dict] = json.load(f)
            raw_nodes: Dict[Hashable, GraphNode] = {}
            for _id, node_dict in nodes.items():
                raw_nodes[_id] = GraphNode.from_dict(node_dict)
        return MusicGraph(graph=graph, node_aliases=aliases, raw_node=raw_nodes)

    @staticmethod
    def merge(graphs: List):
        # TODO: do the merging of multiple graphs
        # Implies resolving artists which have different ids because different platforms
        ...
