# YouTube Liked Songs to Spotify Playlist

This Python script retrieves the songs that you have liked on YouTube and adds them to a Spotify playlist. The script uses the YouTube Data API to retrieve the user's liked videos and identifies the songs in those videos. It then uses the Spotify Web API to search for the songs and add them to a playlist.

## Getting Started

To use this script, you will need to set up a project in the Google Cloud Console and obtain API credentials for the YouTube Data API. You will also need to create a Spotify app and obtain API credentials for the Spotify Web API. You can then add the API credentials to the `client_secrets.json` file.

### Setting up the Google Cloud Platform Secret

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Enable the YouTube Data API for your project.
4. Create credentials for a new OAuth 2.0 client ID.
5. Select "Desktop app" as the application type.
6. Download the client secret JSON file and save it as `client_secret.json` in the same directory as `yt.py`.
7. Open the `client_secret.json` file in a text editor and add the following lines to the file, replacing `your_youtube_client_id` and `your_youtube_client_secret` with your actual YouTube client ID and client secret:

```json
"youtube_client_id": "your_youtube_client_id",
"youtube_client_secret": "your_youtube_client_secret"
```

### Usage

To run the script, simply execute the `main.py` file:

```bash
python main.py
```


The script will prompt you to authorize access to your YouTube account and will then retrieve your liked songs and add them to a Spotify playlist.

### Dependencies

This script requires the following Python packages:

- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- spotipy

You can install these packages using pip:
  
  ```bash
  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client spotipy
  ```

Or you can download all of the dependencies by running the following command in the same directory as `yt.py`:

```bash
pip install -r requirements.txt
```


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

