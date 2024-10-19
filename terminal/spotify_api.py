import spotipy 
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="http://localhost:8888/callback", 
    scope="user-modify-playback-state,user-read-playback-state, user-read-currently-playing"
))

user_data = sp.current_user()
print(f"Logged in as: {user_data['display_name']}")

current_playback = sp.current_playback()

if current_playback is not None and current_playback['is_playing']:
    track = current_playback['item']
    device = current_playback['device']
    print(f"Currently playing: {track['name']} from {track['album']['name']} by {track['artists'][0]['name']} on {device['name']}")
else:
    print("No track is currently playing.")

#devices = sp.devices()['devices']
#for i in devices:
#    print(i['name'], i['id'])

song_name = input("Please enter a song name: ") 
results = sp.search(q=song_name, type='track', limit=1)

if results['tracks']['items']:
    track = results['tracks']['items'][0]
    track_uri = track['uri']
sp.start_playback(uris=[track_uri])