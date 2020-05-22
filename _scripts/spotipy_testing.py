#!/usr/local/bin/python3
# Michelle Tanco - michelle.tanco@gmail.com
# Debugging Spotipy stuff


from spotipy import util
from spotipy import Spotify


mtanco = "1238655357"
my_token = util.prompt_for_user_token(username=mtanco,
                                      scope="user-read-recently-played",
                                      redirect_uri="http://127.0.0.1:12345")

if my_token:
    sp = Spotify(auth=my_token)
    results = sp.current_user_recently_played()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", mtanco)
