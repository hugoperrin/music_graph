# Music Graph library

* abstracts music library graph for any type of data and sources.
* intended use: recommending system helper, and data visualization of personnal library.

## What's done :heavy_check_mark:

- [x] data fetcher for spotify API using [spotipy](https://github.com/plamere/spotipy)
- [x] data fetcher for tidal API using [tidalapi](https://tidalapi.netlify.app/index.html)

## TODOs

* [ ] merging different APIs graphs
* [ ] base the graph implementation from the naive current implementation to boost/networkx graph in order to use existing fast graph algorithms.
* [ ] clustering of graph to create playlists and visualisation
* [ ] recommendation based on textual features (artist bio + playlist description + lyrics)
* [ ] recommendation based on extracted features (based solely on graph nodes and relationship + metadata)
* [ ] recommendation based on musical features (music sample)

## Idea

1st Step: [Graph creation](docs/general/graph_creation.md)
Possible 2nd steps:

* [clustering to create playlists](docs/clustering/clustering.md)
* [recommendations using that graph](docs/recommendation/recommendation_general.md)
