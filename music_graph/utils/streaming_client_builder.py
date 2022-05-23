from typing import Tuple


from music_graph.abstract.client import AbstractStreamingAPIClient
from music_graph.data.general_fetcher import GraphBuildingModeEnum


class StreamingClientAPIClientBuilder:
    @staticmethod
    def from_env() -> Tuple[AbstractStreamingAPIClient, GraphBuildingModeEnum]:
        # TODO: do from env loading
        ...
