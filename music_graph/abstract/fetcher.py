from abc import abstractmethod
from music_graph.datamodel.graph.graph import MusicGraph


class AbstractFetcher:
    @abstractmethod
    def fetch_graph(self) -> MusicGraph:
        ...
