
import concurrent.futures
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotifyClientId = "ae3f44ab6e8c4df685fd5c49e8bbe441"
spotifyCLientSecret = "a8702350ce9542388b23af7f31325d01"
client_secrets_file = "client_secret.json"

client_credentials_manager = SpotifyClientCredentials(client_id=spotifyClientId, client_secret=spotifyCLientSecret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up the OAuth2 client
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()

# Set up the YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Define a function to retrieve a page of liked videos and identify the songs
def get_liked_songs_page(page_token):
    request = youtube.videos().list(
        part="snippet",
        myRating="like",
        maxResults=50,
        pageToken=page_token
    )
    response = request.execute()
    liked_songs = []
    for video in response["items"]:
        if "categoryId" in video["snippet"] and video["snippet"]["categoryId"] == "10":
            liked_songs.append(video)
    return liked_songs, response.get("nextPageToken")

# Call the API to retrieve the user's liked videos and identify the songs
liked_songs = []
next_page_token = None
with concurrent.futures.ThreadPoolExecutor() as executor:
    while True:
        futures = [executor.submit(get_liked_songs_page, next_page_token)]
        for future in concurrent.futures.as_completed(futures):
            songs, next_page_token = future.result()
            liked_songs.extend(songs)
        if not next_page_token:
            break

# Print the titles of the user's liked songs
for song in liked_songs:
    print(song["snippet"]["title"])
