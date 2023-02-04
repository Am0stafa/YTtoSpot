#It goes through your liked videos YouTube, filters the songs, searches them on Spotify, creates a new Spotify playlist with all the available songs

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotifyClientId = "ae3f44ab6e8c4df685fd5c49e8bbe441"
spotifyCLientSecret = "a8702350ce9542388b23af7f31325d01"

client_credentials_manager = SpotifyClientCredentials(client_id=spotifyClientId, client_secret=spotifyCLientSecret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Get the liked videos from YouTube


import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

class CreatePlayList:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}
    

    #Log into Youtube
    def get_youtube_client(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    #log into Spotify
    
        

if __name__ == '__main__':
    cp = CreatePlayList()
    print(cp.youtube_client)