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
import pandas as pd
from tabulate import tabulate

from spotipy.oauth2 import SpotifyClientCredentials
import time

# Spotify User data
from config import username, client_id, client_secret, redirect

# Export calls to validate credentials through Spotify's Web Dev API
os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = redirect

# Erase cache and prompt user for permission
scope = "user-top-read"
try:
    token = utl.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = utl.prompt_for_user_token(username, scope)

# Create spotify object
spotify_object = spotipy.Spotify(auth=token)

# User data
user_data = spotify_object.current_user()
display_name = user_data["display_name"]
followers = user_data["followers"]["total"]

# Basic search loop
# run_loop = True
# while run_loop == True:
#     print()
#     print(f">>> Welcome {display_name}!")
#     print(f">>> You currently have {followers} followers.")
#     print()
#     print(f">>> Choices:")
#     print(f">> 0 - Search for an artist")
#     print(f">> 1 - Exit")
#     print()
#     choice = input(">>> Make a selection: ")
#
#     # End the program
#     if choice == "1":
#         run_loop = False
#
#     # Search for an artist
#     if choice == "0":
#         print()
#         artist_name = input("Artist name: ")
#         print()
#
#         # Return search results
#         artist_results = spotify_object.search(artist_name, 1, 0, "artist")
#         pprint(artist_results)

# Get top artists
# if token:
#     spotify_object.trace = False
#     ranges = ["short_term", "medium_term", "long_term"]
#     for range in ranges:
#         print(f"range: {range}")
#         results = spotify_object.current_user_top_artists(time_range=range, limit=50)
#         for i, item in enumerate(results["items"]):
#             print(i, item["name"], item["popularity"], item["followers"]["total"], str(len(item["genres"])))
#         print()
# else:
#     print(f"Can't get token for {username}")

# Short term data frame
# Defaults
rank = []
popularity = []
artists = []
total_followers = []
genres = []
artist_id = []
total_albums = []
# total_markets = []

# Populate lists
if token:
    spotify_object.trace = False
    print(f"Range: short_term")

    # Storing searches as json objects
    results = spotify_object.current_user_top_artists(time_range="short_term", limit=50)

    for i, item in enumerate(results["items"]):
        rank.append(i + 1)
        artists.append(item["name"])
        popularity.append(item["popularity"])
        total_followers.append(item["followers"]["total"])
        genres.append(str(len(item["genres"])))
        artist_id.append(item["id"])
        artist_album_results = spotify_object.artist_albums(item["id"], limit=50)
        total_albums.append(len(artist_album_results["items"]))
    print()
    # pprint(results)
    # print()
else:
    print(f"Can't get token for {username}")

# Creating the df
spotify_df = pd.DataFrame(
    {
        "Rank": [rank for rank in rank],
        "Artist": [artist for artist in artists],
        "Popularity": [pop for pop in popularity],
        "Total Followers": [fol for fol in total_followers],
        "Number of Genres": [gen for gen in genres],
        "Number of Albums": [album for album in total_albums],
        "Artist ID": [i for i in artist_id]

    })

# Printing table
spotify_df = spotify_df.set_index("Rank")
print(tabulate(spotify_df, headers='keys', tablefmt='psql'))
print()

# Testing Space: Artist album work
test_results = spotify_object.artist_albums("45eNHdiiabvmbp4erw26rg", limit=1)
pprint(test_results)
print(len(test_results["items"][0]["available_markets"]))

