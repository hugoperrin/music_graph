import json
from dataclasses import dataclass
from typing import Dict, List, Optional

from music_graph.abstract.client import AbstractStreamingAPIClient
from music_graph.abstract.fetcher import AbstractFetcher
from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.base_data import BaseData
from music_graph.datamodel.graph.graph import MusicGraph
from music_graph.datamodel.graph.node import GraphNode, NeighborData
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData
from music_graph.datamodel.user_info import UserInfo


@dataclass()
class GraphConfig:
    has_artists: bool = True
    has_albums: bool = True
    has_tracks: bool = True
    has_playlists: bool = False
    augment_graph: bool = True
    base_w: float = 1.0
    base_cap: float = 1.0
    enhance_w: float = 1.0
    enhance_cap: float = 1.0

    def to_dict(self) -> Dict:
        return {
            "has_artists": self.has_artists,
            "has_albums": self.has_albums,
            "has_tracks": self.has_tracks,
            "has_playlists": self.has_playlists,
            "augment_graph": self.augment_graph,
            "base_w": self.base_w,
            "base_cap": self.base_cap,
            "enhance_w": self.enhance_w,
            "enhance_cap": self.enhance_cap,
        }

    def write(self, path: str):
        with open(path, "w") as f:
            json.dump(
                self.to_dict(), f,
            )

    @staticmethod
    def read(path: Optional[str] = None):
        if path is None:
            return GraphConfig()
        with open(path, "r") as f:
            dict_data: Dict = json.load(f)
        return GraphConfig(
            has_artists=dict_data.get("has_artists", True),
            has_albums=dict_data.get("has_albums", True),
            has_tracks=dict_data.get("has_tracks", True),
            has_playlists=dict_data.get("has_playlists", False),
            augment_graph=dict_data.get("augment_graph", True),
            base_cap=dict_data.get("base_cap", 1.0),
            base_w=dict_data.get("base_w", 1.0),
            enhance_cap=dict_data.get("enhance_cap", 1.0),
            enhance_w=dict_data.get("enhance_w", 1.0),
        )


class GeneralFetcher(AbstractFetcher):
    def __init__(self, client: AbstractStreamingAPIClient) -> None:
        self.client = client

    def fetch_graph(
        self, user_id: str, config_path: Optional[str] = None
    ) -> MusicGraph:
        config: GraphConfig = GraphConfig.read(config_path)
        user_info = self.client.get_user_info(user_id=user_id)
        graph = self.fetch_positive_graph(user_info=user_info, config=config)
        if config.augment_graph:
            graph = self.enhance_recursive_graph(graph=graph, config=config)
        return graph

    def fetch_positive_graph(
        self, user_info: UserInfo, config: GraphConfig,
    ) -> MusicGraph:
        graph: MusicGraph = MusicGraph()
        if config.has_albums:
            graph = self.add_albums(user_info, graph, config)
        if config.has_artists:
            graph = self.add_artists(user_info, graph, config)
        if config.has_playlists:
            graph = self.add_playlists(user_info, graph, config)
        if config.has_tracks:
            graph = self.add_tracks(user_info, graph, config)
        return graph

    def enhance_recursive_graph(
        self, graph: MusicGraph, config: GraphConfig,
    ) -> MusicGraph:
        if config.has_albums:
            self.enhance_albums(graph, config)
        if config.has_artists:
            self.enhance_artists(graph, config)
        if config.has_playlists:
            self.enhance_playlists(graph, config)
        if config.has_tracks:
            return self.enhance_tracks(graph, config)
        return graph

    def add_artists(
        self, user_info: UserInfo, graph: MusicGraph, config: GraphConfig,
    ) -> MusicGraph:
        graph.add_node(GraphNode("root", user_info, neighbor_ids=[], value=1.0))
        for artist_id in user_info.artist_ids:
            artist_data: ArtistData = self.client.get_artist(artist_id=artist_id)
            graph.add_node(
                node=GraphNode(
                    id=artist_data.id, object=artist_data, neighbor_ids=[], value=1.0,
                )
            )
            graph.add_edge("root", artist_data.id, w=config.base_w, cap=config.base_cap)

        return graph

    def enhance_artists(self, graph: MusicGraph, config: GraphConfig) -> MusicGraph:
        artist_ids: List[str] = graph.raw_node["root"].object.artist_ids  # type: ignore
        for art_id in artist_ids:
            ref_data: ArtistData = graph.raw_node[art_id].object  # type: ignore
            neighbor_ids = self.client.get_artist_neighbors(ref_data.data_id)
            graph.raw_node[art_id].neighbor_ids += [
                NeighborData(
                    id=n, edge_weight=config.enhance_w, edge_cap=config.enhance_cap
                )
                for n in neighbor_ids
            ]
            for n_id in neighbor_ids:
                data: ArtistData = self.client.get_artist(artist_id=n_id)
                graph.add_node(
                    node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
                )
                graph.add_edge(
                    art_id, data.id, w=config.enhance_w, cap=config.enhance_cap,
                )
        return graph

    def add_albums(
        self, user_info: UserInfo, graph: MusicGraph, config: GraphConfig,
    ) -> MusicGraph:
        graph.add_node(GraphNode("root", user_info, neighbor_ids=[], value=1.0))
        for album_id in user_info.saved_album_ids:
            data: AlbumData = self.client.get_album(album_id=album_id)
            graph.add_node(
                node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
            )
            graph.add_edge("root", data.id, w=config.base_w, cap=config.base_cap)

        return graph

    def enhance_albums(self, graph: MusicGraph, config: GraphConfig) -> MusicGraph:
        album_ids: List[str] = graph.raw_node["root"].object.album_ids  # type: ignore
        for alb_id in album_ids:
            ref_data: BaseData = graph.raw_node[alb_id].object  # type: ignore
            neighbor_ids = self.client.get_album_neighbors(ref_data.data_id)
            graph.raw_node[alb_id].neighbor_ids += [
                NeighborData(
                    id=n, edge_weight=config.enhance_w, edge_cap=config.enhance_cap
                )
                for n in neighbor_ids
            ]
            for n_id in neighbor_ids:
                data: AlbumData = self.client.get_album(album_id=n_id)
                graph.add_node(
                    node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
                )
                graph.add_edge(
                    alb_id, data.id, w=config.enhance_w, cap=config.enhance_cap,
                )
        return graph

    def add_playlists(
        self, user_info: UserInfo, graph: MusicGraph, config: GraphConfig,
    ) -> MusicGraph:
        graph.add_node(GraphNode("root", user_info, neighbor_ids=[], value=1.0))
        for playlist_id in user_info.playlist_ids:
            data: PlaylistData = self.client.get_playlist(playlist_id=playlist_id)
            graph.add_node(
                node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
            )
            graph.add_edge("root", data.id, w=config.base_w, cap=config.base_cap)

        return graph

    def enhance_playlists(self, graph: MusicGraph, config: GraphConfig) -> MusicGraph:
        playlist_ids: List[str] = graph.raw_node["root"].object.playlist_ids  # type: ignore
        for plist_id in playlist_ids:
            ref_data: BaseData = graph.raw_node[plist_id].object  # type: ignore
            neighbor_ids = self.client.get_playlist_neighbors(ref_data.data_id)
            graph.raw_node[plist_id].neighbor_ids += [
                NeighborData(
                    id=n, edge_weight=config.enhance_w, edge_cap=config.enhance_cap
                )
                for n in neighbor_ids
            ]
            for n_id in neighbor_ids:
                data: AlbumData = self.client.get_album(album_id=n_id)
                graph.add_node(
                    node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
                )
                graph.add_edge(
                    plist_id, data.id, w=config.enhance_w, cap=config.enhance_cap,
                )
        return graph

    def add_tracks(
        self, user_info: UserInfo, graph: MusicGraph, config: GraphConfig,
    ) -> MusicGraph:
        graph.add_node(GraphNode("root", user_info, neighbor_ids=[], value=1.0))
        for track_id in user_info.saved_track_ids:
            data: TrackData = self.client.get_track(track_id=track_id)
            graph.add_node(
                node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
            )
            graph.add_edge("root", data.id, w=config.base_w, cap=config.base_cap)

        return graph

    def enhance_tracks(self, graph: MusicGraph, config: GraphConfig) -> MusicGraph:
        track_ids: List[str] = graph.raw_node["root"].object.track_ids  # type: ignore
        for track_id in track_ids:
            ref_data: BaseData = graph.raw_node[track_id].object  # type: ignore
            neighbor_ids = self.client.get_track_neighbors(ref_data.data_id)
            graph.raw_node[track_id].neighbor_ids += [
                NeighborData(
                    id=n, edge_weight=config.enhance_w, edge_cap=config.enhance_cap
                )
                for n in neighbor_ids
            ]
            for n_id in neighbor_ids:
                data: AlbumData = self.client.get_album(album_id=n_id)
                graph.add_node(
                    node=GraphNode(id=data.id, object=data, neighbor_ids=[], value=1.0)
                )
                graph.add_edge(
                    track_id, data.id, w=config.enhance_w, cap=config.enhance_cap,
                )
        return graph


if __name__ == "__main__":
    import fire
    from music_graph.utils.streaming_client_builder import (
        StreamingClientAPIClientBuilder,
    )

    client = StreamingClientAPIClientBuilder.from_env()
    fetcher = GeneralFetcher(client=client)
    fire.Fire(fetcher)
