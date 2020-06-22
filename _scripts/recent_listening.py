#!/usr/local/bin/python3
# Michelle Tanco - michelle.tanco@gmail.com
# Create Markdown of Spotify Play History

from spotipy import Spotify
from spotipy import util
import pandas as pd

# Get authorization token for this user - resfreshes or asks for permission as needed
my_token = util.prompt_for_user_token(username="1238655357", # Michelle's ID
                                      scope="user-read-recently-played", # allows us to see recently played songs
                                      redirect_uri="http://127.0.0.1:12345") # URL in our app

# Object for interacting with spotify user
spotify = Spotify(auth=my_token)

# list of last 50 songs
last_songs_dict = spotify.current_user_recently_played()['items']

print("*** MARKDOWN LIST OF ARTISTS WITH LINKS ***")
# frame to hold artists
artists = pd.DataFrame()

# Get information for all tracks
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


# get the genres I've been listening to the most
print("\n\n *** MARKDOWN LIST OF MOST COMMON GENRES ***")

genre_counts = dict()

# each song
for s in last_songs_dict:

    # each artist involved in the song
    for a in s["track"]["artists"]:
        artist_uri = a["uri"]

        genres = spotify.artist(artist_uri)['genres']

        # each genre associated with the artist
        for i in genres:
            genre_counts[i] = genre_counts.get(i, 0) + 1

genre_counts = pd.DataFrame(list(genre_counts.items()), columns=['genre', 'count'])
genre_counts = genre_counts.sort_values("count", ascending=False)

top_10 = genre_counts["genre"].head(10)

for g in top_10:
    print("*", g)