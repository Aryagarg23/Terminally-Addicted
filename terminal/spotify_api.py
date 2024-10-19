import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",  # Your client ID
    client_secret="",  # Your client secret
    redirect_uri="http://localhost:8888/callback",
    scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing"
))

user_data = sp.current_user()
print(f"Logged in as: {user_data['display_name']}")

current_playback = sp.current_playback()

if current_playback is not None and current_playback['is_playing']:
    track = current_playback['item']
    device = current_playback['device']
    print(f"Currently playing: {track['name']} from {track['album']['name']} by {track['artists'][0]['name']} on {device['name']}")
    
    # Assuming there is a queue, get the track list
    queue = sp.current_playback()['items']  # Fetch the current queue
    current_index = None
    
    if queue:
        for i, item in enumerate(queue):
            if item['id'] == track['id']:
                current_index = i
                break

        if current_index is not None and current_index + 1 < len(queue):
            # Play the next song in the queue
            next_track = queue[current_index + 1]
            sp.start_playback(uris=[next_track['uri']])
            print(f"Playing next track: {next_track['name']} by {next_track['artists'][0]['name']}")
        else:
            print("No next track in the queue. Searching for new tracks.")
            # No next track, search for new tracks
else:
    print("No track is currently playing. Searching for new tracks.")

# Prompt user for a song name or play a random one
song_name = input("Please enter a song name (or press Enter to play a random track): ")

if song_name:
    results = sp.search(q=song_name, type='track', limit=20)
    
    if results['tracks']['items']:
        # Shuffle the search results
        shuffled_tracks = random.sample(results['tracks']['items'], len(results['tracks']['items']))
        # Start playback with the first track in shuffled results
        track_to_play = shuffled_tracks[0]
        track_uri = track_to_play['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Playing: {track_to_play['name']} by {track_to_play['artists'][0]['name']}")
    else:
        print("No tracks found for your search.")
else:
    # Play a random track from a broader search if no song name is provided
    random_results = sp.search(q='*', type='track', limit=50)  # Search for a wider range of tracks
    if random_results['tracks']['items']:
        random_track = random.choice(random_results['tracks']['items'])
        track_uri = random_track['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Playing a random track: {random_track['name']} by {random_track['artists'][0]['name']}")
    else:
        print("No random tracks found.")
