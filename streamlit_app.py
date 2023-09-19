import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import os

client_id = os.environ.get('YOUR_CLIENT_ID')
client_secret = os.environ.get('YOUR_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

st.title("Travel Through Time: A Musical Journey")
year = st.slider("Select a year to explore music:", 1950, 2020)
limit = st.slider("Number of tracks to fetch:", 10, 50)

def get_tracks_from_year(year, limit=50):
    query = f'year:{year}'
    results = sp.search(q=query, type='track', limit=limit)
    tracks = results['tracks']['items']
    return tracks

tracks = get_tracks_from_year(year, limit)

for track in tracks:
    album_cover_url = track['album']['images'][0]['url']  # Extract the album cover URL (largest image)
    
    # Create two columns: one for the image and one for the track details.
    col1, col2 = st.columns([1, 3])  # Adjust the ratio if needed
    
    with col1:
        st.image(album_cover_url, use_column_width=True)  # Display the album cover
    
    with col2:
        st.write(f"Track: {track['name']} by {track['artists'][0]['name']}")  # Display track details
