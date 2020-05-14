#!/usr/local/bin/python3
# Michelle Tanco - michelle.tanco@gmail.com
# Create Markdown of Spotify Play History

from spotipy import Spotify
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Please include your Spotify Token!")
    print("./<file_name.py> $SPOTIFY_TOKEN")
    sys.exit

spotify = Spotify(auth=str(sys.argv[1]))

last_songs_dict = spotify.current_user_recently_played()['items']

artists = pd.DataFrame()

# Look at each track
for s in last_songs_dict:
    # Look at each artist that contributed to the track
    for a in s['track']['artists']:
        # save artist name, spotify reference uri, and link to their spotify page
        artists = artists.append(pd.DataFrame([[
            a["name"], a["uri"], a["external_urls"]["spotify"]
        ]]))

artists.columns = ["artist_name", "artist_uri", "artist_page"]

artist_counts = artists.groupby(["artist_name", "artist_uri", "artist_page"]).size().reset_index()

artist_counts.columns = ["artist_name", "artist_uri", "artist_page", "song_count"]

for i, r in artist_counts.sort_values("song_count", ascending=False).iterrows():
    print("* [" + r["artist_name"] + "](" + r["artist_page"] + ")")
