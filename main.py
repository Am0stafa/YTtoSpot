import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
import spotipy.util as util
import concurrent.futures
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

client_secrets_file = "client_secret.json"

def get_liked_songs(youtube_credentials):
    # Set up the YouTube Data API client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=youtube_credentials)

    # Call the YouTube API to retrieve the user's liked videos and identify the songs
    liked_songs = []
    next_page_token = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            futures = [executor.submit(get_liked_songs_page, youtube, next_page_token)]
            for future in concurrent.futures.as_completed(futures):
                songs, next_page_token = future.result()
                liked_songs.extend(songs)
            if not next_page_token:
                break
    return liked_songs

def get_liked_songs_page(youtube, page_token):
    request = youtube.videos().list(
        part="snippet",
        myRating="like",
        maxResults=50,
        pageToken=page_token
    )
    response = request.execute()
    songs = []
    for video in response["items"]:
        if "categoryId" in video["snippet"] and video["snippet"]["categoryId"] == "10":
            songs.append(video)
    next_page_token = response.get("nextPageToken")
    return songs, next_page_token

# def create_spotify_playlist(spotify, playlist_name, playlist_description):
#     # Create the playlist if it doesn't already exist
#     playlist_id = None
#     for playlist in spotify.current_user_playlists()["items"]:
#         if playlist["name"] == playlist_name:
#             playlist_id = playlist["id"]
#             break
#     if not playlist_id:
#         playlist = spotify.user_playlist_create(spotify.current_user()["id"], playlist_name, public=True, description=playlist_description)
#         playlist_id = playlist["id"]
#     return playlist_id

def create_spotify_playlist(spotify, playlist_name, playlist_description):
    # Create the playlist if it doesn't already exist
    playlist_id = None
    for playlist in spotify.current_user_playlists()["items"]:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            break
    if not playlist_id:
        playlist = spotify.user_playlist_create(spotify.current_user()["id"], playlist_name, public=True, description=playlist_description)
        playlist_id = playlist["id"]
    return playlist_id


def add_songs_to_spotify_playlist(spotify, playlist_id, liked_songs):
    # Add the songs to the playlist
    spotify_tracks = []
    for song in liked_songs:
        query = song["snippet"]["title"]
        results = spotify.search(q=query, type="track", limit=1)
        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            spotify_tracks.append(track["uri"])
    if spotify_tracks:
        spotify.user_playlist_add_tracks(spotify.current_user()["id"], playlist_id, spotify_tracks)

# Set up the OAuth2 client for YouTube
youtube_scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youtube_flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, youtube_scopes)
youtube_credentials = youtube_flow.run_console()

# Get the user's liked songs from YouTube
liked_songs = get_liked_songs(youtube_credentials)

# Set up the OAuth2 client for Spotify
spotify_scopes = ["playlist-modify-public"]
spotify_client_id = "ae3f44ab6e8c4df685fd5c49e8bbe441"
spotify_client_secret = "a8702350ce9542388b23af7f31325d01"
redirect_uri = "https://example.com/callback"
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=redirect_uri, scope=spotify_scopes))

# Create the Spotify playlist and add the songs to it

# playlist_name = "My Liked Songs"
# playlist_description = "A playlist of my liked songs on YouTube"
# playlist_id = create_spotify_playlist(spotify, playlist_name, playlist_description)
# add_songs_to_spotify_playlist(spotify, playlist_id, liked_songs)

# Create the Spotify playlist and add the songs to it
playlist_name = "My Liked Songs"
playlist_description = "A playlist of my liked songs on YouTube"
playlist_id = create_spotify_playlist(spotify, playlist_name, playlist_description)
add_songs_to_spotify_playlist(spotify, playlist_id, liked_songs)

# Construct the playlist URL and print it
playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
print(f"Your Spotify playlist is ready: {playlist_url}")
