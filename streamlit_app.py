import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import googleapiclient.discovery
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery


# Spotify setup
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ... and so on for other keys




# Define the scopes
scopes = ["https://www.googleapis.com/auth/youtube"]

# Create the OAuth flow
flow = Flow.from_client_config(
    client_config={
        "web": st.secrets["web"]
    },
    scopes=scopes
)

# Run the console flow
credentials = flow.run_console()

# Build the YouTube API client
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

st.title("Travel Through Time: A Musical Journey")
year = st.slider("Select a year to explore music:", 1950, 2020)
limit = st.slider("Number of tracks to fetch:", 10, 50)

def get_tracks_from_year(year, limit=50):
    query = f'year:{year}'
    results = sp.search(q=query, type='track', limit=limit)
    tracks = results['tracks']['items']
    return tracks

tracks = get_tracks_from_year(year, limit)
tracks_sorted_by_popularity = sorted(tracks, key=lambda x: x['popularity'], reverse=True)

# Custom CSS to set the background color to green
st.markdown("""
    <style>
        body {
            background-color: #4CAF50;  # This is a shade of green
        }
    </style>
    """, unsafe_allow_html=True)

for track in tracks_sorted_by_popularity:
    album_cover_url = track['album']['images'][1]['url']
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image(album_cover_url, width=100)
    
    with col2:
        st.markdown(f"**Track:** {track['name']} \n**Artist:** {track['artists'][0]['name']} (Popularity: {track['popularity']})")

# Add a button in Streamlit to create the YouTube playlist
if st.button('Make a YouTube Playlist'):
    playlist_id = create_youtube_playlist(f"Music from {year}")
    video_ids = [search_youtube(f"{track['name']} {track['artists'][0]['name']}") for track in tracks_sorted_by_popularity]
    
    for video_id in video_ids:
        add_video_to_playlist(playlist_id, video_id)
    
    st.markdown(f'YouTube playlist created! [View Playlist](https://www.youtube.com/playlist?list={playlist_id})', unsafe_allow_html=True)
