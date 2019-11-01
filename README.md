# Spotify-ML-Fun

## Background

My main plan for this project is to experiment with Spotify's Web API. I plan to start pulling as much data as I can, 
without putting too many constraints on the type of data. With a large data set, I hope to practice implementing various 
Machine Learning algorithms. The variety of data will help me practice eliminating parts of data sets that are not 
similar.

## Main Files
* localhost_test.py is local server test file - Not in use
    * Contains basic information
* playground.py is the main file that I will be using.
	* Spotipy's library allows me to easily access public spotify data, with which I will perform my data analysis
    * Connected to Spotify's Web API through Spotipy library
        * All export calls are called within the file, terminal credential calls are not needed
    * Have completed a dry run with PCA, no real purpose other than to test dimensional reduction
        * The API limits pulls to 50 items, therefore data is severely limited
        * Principal Component 1 contains 51.9182% of the variance and Component 2 contains 30.8413%; therefore the 
        total retained variance is: 82.7595%