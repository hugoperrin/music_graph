# Music Graph library

* abstracts music library graph for any type of data and sources.
* intended use: recommending system helper, and data visualization of personnal library.

## What's done :heavy_check_mark:

- [x] data fetcher for spotify API using [spotipy](https://github.com/plamere/spotipy)
- [x] data fetcher for tidal API using [tidalapi](https://tidalapi.netlify.app/index.html)

## TODOs

* [ ] base the graph implementation from the naive current implementation to boost/networkx graph in order to use existing fast graph algorithms.
* [ ] merging different APIs graphs
* [ ] clustering of graph to create playlists and visualisation
* [ ] recommendation based on extracted features (based solely on graph nodes and relationship + metadata)
* [ ] recommendation based on textual features (artist bio + playlist description + lyrics)
* [ ] recommendation based on musical features (music sample)
