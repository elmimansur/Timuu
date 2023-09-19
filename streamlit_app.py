import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import os
from googleapiclient.discovery import build

# Spotify setup
client_id = os.environ.get('YOUR_CLIENT_ID')
client_secret = os.environ.get('YOUR_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# YouTube setup
ydevkey = os.environ.get('YOUR_YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=ydevkey)

def search_youtube(track_name):
    """Search for a track on YouTube and return the video URL."""
    request = youtube.search().list(q=track_name, part='id', maxResults=1)
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"

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

# Add a button in Streamlit to create the YouTube mix
if st.button('Make a YouTube Mix'):
    video_urls = [search_youtube(f"{track['name']} {track['artists'][0]['name']}") for track in tracks_sorted_by_popularity]
    for url in video_urls:
        st.markdown(f'<a href="{url}" target="_blank">{url}</a>', unsafe_allow_html=True)
