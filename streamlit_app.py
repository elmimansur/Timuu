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
# Sort tracks by popularity in descending order
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
    album_cover_url = track['album']['images'][1]['url']  # Use a smaller image for the album cover
    
    # Create two columns: one for the image and one for the track details.
    col1, col2 = st.columns([1, 4])  # Adjust the ratio to make the image column smaller
    
    with col1:
        st.image(album_cover_url, width=100)  # Set width to adjust the size of the album cover
    
    with col2:
        st.write(f"Track: {track['name']} by {track['artists'][0]['name']} (Popularity: {track['popularity']})")  # Display track details with popularity
