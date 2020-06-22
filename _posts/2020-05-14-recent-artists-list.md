# Spotify Recently Played List!

I want to create a dynamicly updated list of artists I've been listening to based on my recent Spotify play history. This blog post is a work in progress as I work on this project :) 

<h2>Table of Contents<span class="tocSkip"></span></h2>
<div class="toc"><ul class="toc-item"><li><span><a href="#Getting-Started" data-toc-modified-id="Getting-Started-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Getting Started</a></span></li><li><span><a href="#Autorization-Token" data-toc-modified-id="Autorization-Token-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Autorization Token</a></span></li><li><span><a href="#User-Play-History" data-toc-modified-id="User-Play-History-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>User Play History</a></span><ul class="toc-item"><li><span><a href="#Last-5-Songs-I-Listened-To" data-toc-modified-id="Last-5-Songs-I-Listened-To-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Last 5 Songs I Listened To</a></span></li><li><span><a href="#Last-Albums-I-Listened-To" data-toc-modified-id="Last-Albums-I-Listened-To-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Last Albums I Listened To</a></span></li></ul></li><li><span><a href="#Create-Markdown-of-Recent-Artists-for-Blog" data-toc-modified-id="Create-Markdown-of-Recent-Artists-for-Blog-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Create Markdown of Recent Artists for Blog</a></span></li></ul></div>


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
# Get authorization token for this user - resfreshes or asks for permission as needed
my_token = util.prompt_for_user_token(username="1238655357", # Michelle's ID
                                      scope="user-read-recently-played", # allows us to see recently played songs
                                      redirect_uri="http://127.0.0.1:12345") # URL in our app
```

## User Play History


```python
# Object for interacting with spotify user
spotify = Spotify(auth=my_token)
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
last_songs.columns = ["song", "artist", "album", "timestamp"]

last_songs["timestamp"] = pd.to_datetime(last_songs["timestamp"])

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
      <th>song</th>
      <th>artist</th>
      <th>album</th>
      <th>timestamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Desire (Setare)</td>
      <td>Bahramji &amp; Mashti</td>
      <td>Sufiyan</td>
      <td>2020-06-21 19:04:55.209000+00:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Om Tara Tuttare [Red Fulka Remix]</td>
      <td>Deva Premal</td>
      <td>Yoga Revolution</td>
      <td>2020-06-21 18:59:35.427000+00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Destiny</td>
      <td>Zero 7</td>
      <td>Simple Things</td>
      <td>2020-06-21 18:54:44.004000+00:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Karma Shabda</td>
      <td>No Noise</td>
      <td>Chakra Lounge Vol. 1</td>
      <td>2020-06-21 18:49:05.679000+00:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>An Ending, a Beginning</td>
      <td>Dustin O'Halloran</td>
      <td>Other Lights</td>
      <td>2020-06-21 18:43:58.726000+00:00</td>
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

#last_albumns.columns = ["artist", "spotify_uri", "album"]

last_albumn_counts = last_albumns.groupby(last_albumns.columns.tolist()).size().reset_index(name ='')
last_albumn_counts.columns = ["artist", "spotify_uri", "album", "song_count"]

last_albumn_counts.head(10)
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
      <th>artist</th>
      <th>spotify_uri</th>
      <th>album</th>
      <th>song_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bahramji &amp; Mashti</td>
      <td>spotify:artist:7JWJ86duJuQx2rcch6ZDf2</td>
      <td>Sufiyan</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DJ Drez</td>
      <td>spotify:artist:5j3iObqG7iT7utWpTTmC7F</td>
      <td>Jahta Beat: The Lotus Memoirs</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Deva Premal</td>
      <td>spotify:artist:2970BxpdOBQmkMit6i9kVF</td>
      <td>Yoga Revolution</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Dillon Reznick</td>
      <td>spotify:artist:6lHuJXIBBEw0n9qOmiWWJY</td>
      <td>Lay Your Head on My Shoulder</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Dustin O'Halloran</td>
      <td>spotify:artist:6UEYawMcp2M4JFoXVOtZEq</td>
      <td>Other Lights</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>East Forest</td>
      <td>spotify:artist:0okmfBroVgFuvvljnUbqPW</td>
      <td>The Education Of The Individual Soul</td>
      <td>2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Egil Nielsen</td>
      <td>spotify:artist:0oZuyZXAZ8zvY3ygyApIHf</td>
      <td>A Goodnight Lullaby</td>
      <td>2</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Felix Scott</td>
      <td>spotify:artist:52P6o31sXSSZBcTHwveYx8</td>
      <td>The More We Get Together</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Howard Peele</td>
      <td>spotify:artist:6pIayvI5bDeyEhT5x7LTTe</td>
      <td>Beauty and the Beast</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Jesse Nielsen</td>
      <td>spotify:artist:28hL1CMeKSmGDu43cUqsWW</td>
      <td>Lullabies on Music Box</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## Genres of Recent Artists


```python
# get dictionary of songs from recent listening
last_songs_dict = spotify.current_user_recently_played()['items']

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

genre_counts = pd.DataFrame(list(genre_counts.items()),columns = ['genre','count']) 
genre_counts = genre_counts.sort_values("count", ascending=False)

top_10 = genre_counts["genre"].head(10)

for g in top_10:
    print("*", g)
```

    * chanson
    * vintage schlager
    * torch song
    * shamanic
    * kirtan
    * calming instrumental
    * healing
    * downtempo
    * world fusion
    * meditation


## Create Markdown of Recent Artists for Blog
Someday, we will want this dynamic, but for now here is the script to create the markdown for our recently listened to artists


```python
# list of last 50 songs
last_songs_dict = spotify.current_user_recently_played()['items']

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
```

    * [Édith Piaf](https://open.spotify.com/artist/1WPcVNert9hn7mHsPKDn7j)
    * [Egil Nielsen](https://open.spotify.com/artist/0oZuyZXAZ8zvY3ygyApIHf)
    * [Ramona Singh](https://open.spotify.com/artist/3MJdWvzpiIvIjvZFwqpTR1)
    * [Ray Mondo](https://open.spotify.com/artist/5Di3vQR47VLSQn0JfAU0AZ)
    * [Robin Swan](https://open.spotify.com/artist/6Di4ALvMopgtmvPy6qzoC7)
    * [Jesse Nielsen](https://open.spotify.com/artist/28hL1CMeKSmGDu43cUqsWW)
    * [Julio Menzel](https://open.spotify.com/artist/68VsLtvEAEljBp5OAXOpCL)
    * [East Forest](https://open.spotify.com/artist/0okmfBroVgFuvvljnUbqPW)
    * [The xx](https://open.spotify.com/artist/3iOvXCl6edW5Um0fXEBRXy)
    * [The Baby Orchestra](https://open.spotify.com/artist/0yPT8hhJnDIpGqedGNyiji)
    * [Stephen Rossi](https://open.spotify.com/artist/3GaNCXDzlQMgcBLTxkHLWW)
    * [Peter Ehrlichmann](https://open.spotify.com/artist/4i2t5SSw1MoiBLrD1Lrslx)
    * [Stefan Holmes](https://open.spotify.com/artist/6m0cGvFoQaNv9sZwELfceb)
    * [Sophie Eichmann](https://open.spotify.com/artist/2kzsfr4PAIwyoSPrBq9Xdx)
    * [Sophie Barker](https://open.spotify.com/artist/5338nAeek8WVCOPNnT7Qv2)
    * [Sia](https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN)
    * [Torben Overgaard](https://open.spotify.com/artist/2wrZRfjoJ5N3f1WyYjbKXL)
    * [Riff's Tunes](https://open.spotify.com/artist/6E1XgE6zuMPt2Tm92Yrl3A)
    * [Tristian Fitzmaurice](https://open.spotify.com/artist/19kUkTgm6469j8Pp2BKyav)
    * [Zero 7](https://open.spotify.com/artist/14H7ag1wpQOsPPQJOD6Dqr)
    * [Ralph Aachen](https://open.spotify.com/artist/0dJtjZpWliouisclYavoGF)
    * [Power Music Workout](https://open.spotify.com/artist/3GghVvugpv9nXQ2YFzZNzN)
    * [Phaeleh](https://open.spotify.com/artist/5NkUpXWkeXspvu7iQQOHhP)
    * [Bahramji & Mashti](https://open.spotify.com/artist/7JWJ86duJuQx2rcch6ZDf2)
    * [No Noise](https://open.spotify.com/artist/6LGoAumoBmeQ7cdGn5VTTD)
    * [Kodomo](https://open.spotify.com/artist/57BliIwnAIqKeI4dbAWwaU)
    * [Deva Premal](https://open.spotify.com/artist/2970BxpdOBQmkMit6i9kVF)
    * [Dillon Reznick](https://open.spotify.com/artist/6lHuJXIBBEw0n9qOmiWWJY)
    * [Dustin O'Halloran](https://open.spotify.com/artist/6UEYawMcp2M4JFoXVOtZEq)
    * [Felix Scott](https://open.spotify.com/artist/52P6o31sXSSZBcTHwveYx8)
    * [Howard Peele](https://open.spotify.com/artist/6pIayvI5bDeyEhT5x7LTTe)
    * [John B. Lund](https://open.spotify.com/artist/7aeRsfmuN284l1Hs1eyVbW)
    * [Khruangbin](https://open.spotify.com/artist/2mVVjNmdjXZZDvhgQWiakk)
    * [Lenox Martin](https://open.spotify.com/artist/472Cau4ZzDrfQR8Xwm4arw)
    * [Musicbox Moments](https://open.spotify.com/artist/0nU5Dw03W7guh3qOjxJ4zC)
    * [Les Compagnons De La Chanson](https://open.spotify.com/artist/0tqfplArnNaPnE2AkNIglR)
    * [Luana Dias Araujo](https://open.spotify.com/artist/7s8KvVp5I0zZ48PSCxjwVF)
    * [MC YOGI](https://open.spotify.com/artist/4dkPtsX0xVdn8gZmdMdFuk)
    * [Martha Blackburn](https://open.spotify.com/artist/0YHFM04rfc7pNp63NLvswp)
    * [Martin Grenelle](https://open.spotify.com/artist/7oBwDTaXpreH9jqXxtH2VP)
    * [Mingmei Hsueh](https://open.spotify.com/artist/2Z1JaXCxqUBOH0Zm2Eyrxq)
    * [DJ Drez](https://open.spotify.com/artist/5j3iObqG7iT7utWpTTmC7F)
    * [Miten](https://open.spotify.com/artist/4jrXM6oLQfV9L458Luwc3P)


## Final Python Script

`./<FILE_NAME.py>`

```python
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
```


```python

```
