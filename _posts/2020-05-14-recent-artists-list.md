
I wanted to create a dynamically updated list of artists I've been listening to based on my recent Spotify play history. This blog post is a work in progress as I work on this project :) 

Currently I have a python script that pulls the last 50 songs I listened to from spotify and makes a list of the artists, ordered by number of songs. The output of the script is currently manually pasted into my `lists.md` page. 

```python
from spotipy import util

from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify

import getpass

import pandas as pd
```

## Getting Started
1. Create a Spotify Developers Account 
2. Createe a new Application to get a client key and client secret - I named my application "Token Please" as I'm not using it for anything other than credentials
3. Installed the Spotipy package: `pip install spotipy`
4. Saved our Application credentials to our bash profile: `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`



## Autorization Token

Obtain an authorization token that we can use with the python and web API:
1. Get your userid by logging into Spotify, select the ... on your profile, click share, and then `copy spotify URI` 
2. Use the permissions we want as scope - ability to see what we've recently listened to
3. Use any valid URL as the redict URI

You will then be asked to log in to spotify (from a new webpage) and approve authorization. This will redirect you to a new webpage, copy this URL and paste in the text box below the `prompt_for_user_token` command which will then print your token.


```python
util.prompt_for_user_token(username="1238655357",
                           scope="user-read-recently-played",
                           redirect_uri='https://www.getpostman.com/oauth2/callback')
```


```python
recent_play_token = getpass.getpass("Enter Your Token:")
```

    Enter Your Token:········


## User Play History


```python
spotify = Spotify(auth=recent_play_token)
```

### Last 5 Songs I Listened To


```python
# get dictionary of songs from recent listening
last_songs_dict = spotify.current_user_recently_played(limit=5)['items']

# create dataframe of key information about each song
last_songs = pd.DataFrame()
for s in last_songs_dict:
    last_songs = last_songs.append(pd.DataFrame([[s['track']['name'], 
                                                  s['track']['artists'][0]['name'], 
                                                  s['track']['album']['name'],
                                                  s['played_at']]]))

last_songs = last_songs.reset_index(drop=True)
last_songs.columns = ["track_name", "artist_name", "album_title", "play_time"]

last_songs["play_time"] = pd.to_datetime(last_songs["play_time"])

last_songs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_name</th>
      <th>artist_name</th>
      <th>album_title</th>
      <th>play_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Let's Get Known</td>
      <td>The Unicorns</td>
      <td>Who Will Cut Our Hair When We're Gone? (Remast...</td>
      <td>2020-05-13 00:14:31.853000+00:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Child Star</td>
      <td>The Unicorns</td>
      <td>Who Will Cut Our Hair When We're Gone? (Remast...</td>
      <td>2020-05-11 22:36:04.881000+00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>The Clap</td>
      <td>The Unicorns</td>
      <td>Who Will Cut Our Hair When We're Gone? (Remast...</td>
      <td>2020-05-11 22:30:42.982000+00:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Jellybones</td>
      <td>The Unicorns</td>
      <td>Who Will Cut Our Hair When We're Gone? (Remast...</td>
      <td>2020-05-11 22:29:16.240000+00:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Sea Ghost</td>
      <td>The Unicorns</td>
      <td>Who Will Cut Our Hair When We're Gone? (Remast...</td>
      <td>2020-05-11 22:26:32.334000+00:00</td>
    </tr>
  </tbody>
</table>
</div>



### Last Albums I Listened To
This is names of albums from recent songs rather than a list of albumns I listened fully to


```python
last_songs_dict = spotify.current_user_recently_played()['items']

last_albumns = pd.DataFrame()
for s in last_songs_dict:
    
    last_albumns = last_albumns.append(pd.DataFrame([[s['track']['artists'][0]['name'], 
                                                      s["track"]["artists"][0]["uri"],
                                                      s['track']['album']['name']]]))

last_albumns.columns = ["artist_name", "artist_uri", "album_title"]

last_albumns = last_albumns.drop_duplicates()
last_albumns = last_albumns.reset_index(drop=True)

last_albumns
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>artist_name</th>
      <th>artist_uri</th>
      <th>album_title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>The Unicorns</td>
      <td>spotify:artist:7L5HH5QtkDe7u2hJ1FUKFo</td>
      <td>Who Will Cut Our Hair When We're Gone? (Remast...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Saves The Day</td>
      <td>spotify:artist:5gWhlJBlLQGLOgYWO8lwCU</td>
      <td>Stay What You Are</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Patti Smith</td>
      <td>spotify:artist:0vYkHhJ48Bs3jWcvZXvOrP</td>
      <td>Horses (Legacy Edition)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Bob Dylan</td>
      <td>spotify:artist:74ASZWbe4lXaubB36ztrGX</td>
      <td>Highway 61 Revisited</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Veruca Salt</td>
      <td>spotify:artist:2QwJQuBekTA4qF7N7uLHDP</td>
      <td>Eight Arms To Hold You</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Jack's Mannequin</td>
      <td>spotify:artist:42aeGx2I3uXINpGqC8L0LD</td>
      <td>Everything In Transit</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Gorillaz</td>
      <td>spotify:artist:3AA28KZvwAUcZuOKwyblJQ</td>
      <td>The Now Now</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Radiohead</td>
      <td>spotify:artist:4Z8W4fKeB5YxbusRsdQVPb</td>
      <td>OK Computer</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Foster The People</td>
      <td>spotify:artist:7gP3bB2nilZXLfPHJhMdvc</td>
      <td>Torches</td>
    </tr>
    <tr>
      <th>9</th>
      <td>The Strokes</td>
      <td>spotify:artist:0epOFNiUfyON9EYx7Tpr6V</td>
      <td>The New Abnormal</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Gorillaz</td>
      <td>spotify:artist:3AA28KZvwAUcZuOKwyblJQ</td>
      <td>Song Machine Episode 2</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Blur</td>
      <td>spotify:artist:7MhMgCo0Bl0Kukl93PZbYS</td>
      <td>Blur [Special Edition]</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Interpol</td>
      <td>spotify:artist:3WaJSfKnzc65VDgmj2zU8B</td>
      <td>Our Love To Admire</td>
    </tr>
  </tbody>
</table>
</div>



## Create Markdown of Recent Artists for Blog
Someday, we will want this dynamic, but for now here is the script to create the markdown for our recently listened to artists


```python
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
    print("* [" + r["artist_name"] + "](" + r["artist_page"] +")")
```

    * [Patti Smith](https://open.spotify.com/artist/0vYkHhJ48Bs3jWcvZXvOrP)
    * [Saves The Day](https://open.spotify.com/artist/5gWhlJBlLQGLOgYWO8lwCU)
    * [The Unicorns](https://open.spotify.com/artist/7L5HH5QtkDe7u2hJ1FUKFo)
    * [Bob Dylan](https://open.spotify.com/artist/74ASZWbe4lXaubB36ztrGX)
    * [Jack's Mannequin](https://open.spotify.com/artist/42aeGx2I3uXINpGqC8L0LD)
    * [Gorillaz](https://open.spotify.com/artist/3AA28KZvwAUcZuOKwyblJQ)
    * [Blur](https://open.spotify.com/artist/7MhMgCo0Bl0Kukl93PZbYS)
    * [Fatoumata Diawara](https://open.spotify.com/artist/4G5ZJny3HvX6Il7eHVfnNC)
    * [Foster The People](https://open.spotify.com/artist/7gP3bB2nilZXLfPHJhMdvc)
    * [Interpol](https://open.spotify.com/artist/3WaJSfKnzc65VDgmj2zU8B)
    * [Jamie Principle](https://open.spotify.com/artist/5obQFNrkFoWB51hm1JTHMw)
    * [Radiohead](https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb)
    * [Snoop Dogg](https://open.spotify.com/artist/7hJcb9fa4alzcOq3EaNPoG)
    * [The Strokes](https://open.spotify.com/artist/0epOFNiUfyON9EYx7Tpr6V)
    * [Veruca Salt](https://open.spotify.com/artist/2QwJQuBekTA4qF7N7uLHDP)


## Final Python Script

`./<FILE_NAME.py> $SPOTIFY_TOKEN`

```python
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

```

