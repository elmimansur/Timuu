import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import os

client_id = os.environ.get('YOUR_CLIENT_ID')
client_secret = os.environ.get('YOUR_CLIENT_SECRET')


client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

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
    st.write(f"Track: {track['name']} by {track['artists'][0]['name']}")
