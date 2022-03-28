from typing import Dict, Hashable
from music_graph.abstract.fetcher import AbstractFetcher
from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.graph.graph import MusicGraph
from music_graph.abstract.client import AbstractStreamingAPIClient


from enum import Enum
from music_graph.datamodel.graph.node import GraphNode
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData

from music_graph.datamodel.user_info import UserInfo


class GraphBuildingModeEnum(Enum):
    ARTIST = "artist"
    TRACK = "track"
    PLAYLIST = "playlist"
    ALBUM = "album"


class GeneralFetcher(AbstractFetcher):
    def __init__(
        self, client: AbstractStreamingAPIClient, graph_building_mode: GraphBuildingModeEnum,
    ) -> None:
        self.client = client
        self.graph_building_mode = graph_building_mode

    def fetch_graph(self, user_id: str) -> MusicGraph:
        user_info = self.client.get_user_info(user_id=user_id)
        graph = self.fetch_positive_graph(user_info=user_info)
        graph = self.enhance_recursive_graph(graph=graph)
        return graph

    def fetch_positive_graph(self, user_info: UserInfo) -> MusicGraph:
        if self.graph_building_mode == GraphBuildingModeEnum.ARTIST:
            return self.build_artist_graph(user_info)
        elif self.graph_building_mode == GraphBuildingModeEnum.ALBUM:
            return self.build_album_graph(user_info)
        elif self.graph_building_mode == GraphBuildingModeEnum.PLAYLIST:
            return self.build_playlist_graph(user_info)
        elif self.graph_building_mode == GraphBuildingModeEnum.TRACK:
            return self.build_track_graph(user_info)

    def enhance_recursive_graph(self, graph: MusicGraph) -> MusicGraph:
        # TODO: do the enhancing recursively by adding nodes which are close to the initial graph, but are not in the initial graph.
        return graph

    def build_artist_graph(self, user_info: UserInfo) -> MusicGraph:
        # TODO: finish the code for music graph construction
        graph: MusicGraph = MusicGraph()
        artist_raw_data: Dict[Hashable, ArtistData] = {}
        for artist_id in user_info.artist_ids:
            artist_data: ArtistData = self.client.get_artist(artist_id=artist_id)
            artist_raw_data[artist_data.id] = artist_data
        for data in artist_raw_data.values():
            neighbor_ids = self.client.get_artist_neighbors(data.id)
            graph.add_node(node=GraphNode(id=data.id, object=data, neighbor_ids=neighbor_ids, value=1.0))
        return graph

    def build_album_graph(self, user_info: UserInfo) -> MusicGraph:
        # TODO: do the code for music graph construction
        raise NotImplementedError

    def build_playlist_graph(self, user_info: UserInfo) -> MusicGraph:
        # TODO: do the code for music graph construction
        graph: MusicGraph = MusicGraph()
        playlist_raw_data: Dict[Hashable, PlaylistData] = {}
        for playlist_id in user_info.artist_ids:
            playlist_data: PlaylistData = self.client.get_playlist(playlist_id=playlist_id)
            playlist_raw_data[playlist_data.id] = playlist_data
        for data in playlist_raw_data.values():
            neighbor_ids = self.client.get_playlist_neighbors(data.id)
            graph.add_node(node=GraphNode(id=data.id, object=data, neighbor_ids=neighbor_ids, value=1.0))
        return graph

    def build_track_graph(self, user_info: UserInfo) -> MusicGraph:
        # TODO: do the code for music graph construction
        graph: MusicGraph = MusicGraph()
        track_raw_data: Dict[Hashable, TrackData] = {}
        for track_id in user_info.top_track_ids:
            track_data: TrackData = self.client.get_track(track_id=track_id)
            track_raw_data[track_data.id] = track_data
        for data in track_raw_data.values():
            neighbor_ids = self.client.get_track_neighbors(data.id)
            graph.add_node(node=GraphNode(id=data.id, object=data, neighbor_ids=neighbor_ids, value=1.0))
        return graph
