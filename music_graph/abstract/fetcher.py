from abc import abstractmethod
from os import path
from typing import List

from music_graph.datamodel.graph.graph import MusicGraph


class AbstractFetcher:
    @abstractmethod
    def fetch_graph(self, user_id: str) -> MusicGraph:
        ...

    def fetch_graph_and_write(self, user_id: str, path: str, *args, **kwargs):
        g = self.fetch_graph(user_id, *args, **kwargs)
        g.write(path)

    def merge_graphs(self, paths: List[str]) -> MusicGraph:
        graphs: List[MusicGraph] = [MusicGraph.read(p) for p in paths]
        return MusicGraph.merge(graphs)

    def merge_graphs_and_write(self, paths: List[str], out_path: str) -> None:
        g: MusicGraph = self.merge_graphs(paths)
        g.write(out_path)
