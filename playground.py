# Dependencies

import requests
import json
from pprint import pprint
import sys
import webbrowser
from json.decoder import JSONDecodeError
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import time

import spotipy
import os
import spotipy.util as utl
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

# Spotify User data
from config import username, client_id, client_secret, redirect

# Scikit-learn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

# Spotify data frame
# Defaults
rank = []
popularity = []
artists = []
total_followers = []
genres = []
artist_id = []
total_albums = []
total_markets = []
avg_tracks = []
popularity_bracket = []

# Populate lists
if token:
    spotify_object.trace = False
    time_range = ["short_term", "medium_term", "long_term"]
    print(f"Range: {time_range[2]}")

    # Storing searches as json objects
    results = spotify_object.current_user_top_artists(time_range=time_range[2], limit=50)

    # Counters
    market_counter = 0
    tracks_counter = 0
    for i, item in enumerate(results["items"]):
        # Basic artist info
        rank.append(i + 1)
        artists.append(item["name"])
        popularity.append(item["popularity"])
        total_followers.append(item["followers"]["total"])
        genres.append(str(len(item["genres"])))
        artist_id.append(item["id"])

        # Artist total albums (limited to 50...)
        artist_album_results = spotify_object.artist_albums(item["id"], limit=50)
        total_albums.append(len(artist_album_results["items"]))

        # Average market size per album
        for market in range(0, len(artist_album_results["items"])):
            market_counter += len(artist_album_results["items"][market]["available_markets"])
        if len(artist_album_results["items"]) > 0:
            total_markets.append(market_counter / len(artist_album_results["items"]))
        else:
            total_markets.append(market_counter / 1)

        # Average number of tracks per album
        for track in range(0, len(artist_album_results["items"])):
            tracks_counter += artist_album_results["items"][track]["total_tracks"]
        if len(artist_album_results["items"]) > 0:
            avg_tracks.append(tracks_counter / len(artist_album_results["items"]))
        else:
            avg_tracks.append(tracks_counter / 1) # or append 0

        # Popularity classification
        if item["popularity"] >= 85:
            popularity_bracket.append("Very Popular")
        elif 70 < item["popularity"] < 85:
            popularity_bracket.append("Popular")
        else:
            popularity_bracket.append("Not Popular")
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
        "Average Number of Markets": [m for m in total_markets],
        "Average Tracks per Album": [t for t in avg_tracks],
        "Popularity Class": [p for p in popularity_bracket]
        # "Artist ID": [i for i in artist_id]

    })

# Printing table
spotify_df = spotify_df.set_index("Rank")
print(tabulate(spotify_df, headers="keys", tablefmt="psql"))
print()

# Principal Component Analysis
features = ["Total Followers", "Number of Genres", "Average Number of Markets", "Average Tracks per Album"]

# Separating out the features
components = spotify_df.loc[:, features].values

# Separating out the target
all_targets = spotify_df.loc[:, ["Popularity Class"]].values

# Standardizing the features
components = StandardScaler().fit_transform(components)

# PCA Projection to 2D
pca = PCA(n_components=2)
principal_components = pca.fit_transform(components)

pca_df = pd.DataFrame(data=principal_components, columns=["Principal Component 1", "Principal Component 2"])
final_df = pd.concat([pca_df, spotify_df[["Popularity Class"]].reset_index()], axis=1)
final_df = final_df.drop(columns=["Rank"])
print(tabulate(final_df, headers="keys", tablefmt="psql"))

# Plotting Analysis
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel("Principal Component 1", fontsize=15)
ax.set_ylabel("Principal Component 2", fontsize=15)
ax.set_title("2 Component PCA", fontsize=20)
targets = ["Very Popular", "Popular", "Not Popular"]
colors = ["r", "g", "b"]
for target, color in zip(targets, colors):
    indicesToKeep = final_df["Popularity Class"] == target
    ax.scatter(final_df.loc[indicesToKeep, "Principal Component 1"],
               final_df.loc[indicesToKeep, "Principal Component 2"],
               c=color, s=50)
ax.legend(targets)
ax.grid()
plt.savefig("2 Component PCA on Artist Popularity.png")
# plt.show()

# Variance
variance = pca.explained_variance_ratio_
comp1_var = round(variance[0] * 100, 4)
comp2_var = round(variance[1] * 100, 4)
total_var = comp1_var + comp2_var
print(f"Component 1 contains {comp1_var}% of the variance and Component 2 contains {comp2_var}%",
      f"The total retained variance is: {total_var}%")


