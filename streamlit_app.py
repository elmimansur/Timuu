import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Spotify setup
client_id = os.environ.get('YOUR_CLIENT_ID')
client_secret = os.environ.get('YOUR_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# YouTube OAuth setup
scopes = ["https://www.googleapis.com/auth/youtube"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("path_to_your_credentials.json", scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def search_youtube(track_name):
    request = youtube.search().list(q=track_name, part='id', maxResults=1)
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return video_id

def create_youtube_playlist(title, description=""):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    return response["id"]

def add_video_to_playlist(playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

# ... [rest of your Streamlit UI code]

# Add a button in Streamlit to create the YouTube playlist
if st.button('Make a YouTube Playlist'):
    playlist_id = create_youtube_playlist(f"Music from {year}")
    video_ids = [search_youtube(f"{track['name']} {track['artists'][0]['name']}") for track in tracks_sorted_by_popularity]
    
    for video_id in video_ids:
        add_video_to_playlist(playlist_id, video_id)
    
    st.markdown(f'YouTube playlist created! [View Playlist](https://www.youtube.com/playlist?list={playlist_id})', unsafe_allow_html=True)
