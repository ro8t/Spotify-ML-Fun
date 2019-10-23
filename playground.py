# Dependencies
import requests
import json
from pprint import pprint
import spotipy
import sys
import os
import webbrowser
import spotipy.util as utl
from json.decoder import JSONDecodeError

# Spotify User data
from config import username, client_id, client_secret, redirect

# Export calls to validate credentials through Spotify's Web Dev API
os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = redirect



# Erase cache and prompt user for permission
try:
    token = utl.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = utl.prompt_for_user_token(username)

# Create spotify object
spotifyObject = spotipy.Spotify(auth=token)


# User data
user_data = spotifyObject.current_user()
pprint(user_data)

followers = user_data["followers"]["total"]
print(f"{username} has {followers} followers on Spotify")