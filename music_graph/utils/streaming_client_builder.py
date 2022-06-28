from music_graph.abstract.client import AbstractStreamingAPIClient


class StreamingClientAPIClientBuilder:
    @staticmethod
    def from_env() -> AbstractStreamingAPIClient:
        # TODO: do from env loading
        ...
