# Dependencies
import requests
import json
from pprint import pprint
import spotipy


#test_url = "https://api.spotify.com/v1/playlists/{1lBm7oc0xhTLO7bMYKnt7o}"
#response = requests.get(test_url).json()
#pprint(response)

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify()

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


