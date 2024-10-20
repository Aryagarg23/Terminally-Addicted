import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os

# Function to load credentials from a text file
def load_credentials_from_txt(file_path):
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                credentials[key] = value
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Please ensure the file exists and is formatted correctly.")
    except ValueError:
        raise ValueError("File format incorrect. Each line should be in the format 'KEY=VALUE'.")
    return credentials

# Load credentials from a text file
credentials_file = "spotify_credentials.txt"
credentials = load_credentials_from_txt(credentials_file)

client_id = credentials.get("SPOTIPY_CLIENT_ID")
client_secret = credentials.get("SPOTIPY_CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("Please set the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in the text file.")

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,  # Your client ID from the text file
    client_secret=client_secret,  # Your client secret from the text file
    redirect_uri="http://localhost:8888/callback",
    scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing"
))

user_data = sp.current_user()
print(f"Logged in as: {user_data['display_name']}")

current_playback = sp.current_playback()
previous_search_results = []  # Initialize a list to store previous search results

# Check if something is currently playing
if current_playback is not None and current_playback['is_playing']:
    track = current_playback['item']
    device = current_playback['device']
    print(f"Currently playing: {track['name']} from {track['album']['name']} by {track['artists'][0]['name']} on {device['name']}")
else:
    print("No track is currently playing. Searching for new tracks.")

# Prompt user for a song name or play a random one
song_name = input("Please enter a song name (or press Enter to play a random track): ")

if song_name:
    results = sp.search(q=song_name, type='track', limit=20)
    
    if results['tracks']['items']:
        # Store the search results for later use
        previous_search_results = results['tracks']['items']

        # Shuffle the search results
        shuffled_tracks = random.sample(previous_search_results, len(previous_search_results))

        # Clear the current queue by skipping the current number of queued tracks
        if current_playback and current_playback.get('context'):
            # Get the current playback context to determine the queue size
            context_uri = current_playback['context']['uri']
            queue_size = sp.current_playback()['queue_length']
            print(f"Current queue size: {queue_size}")

            # Skip the number of tracks in the queue
            for _ in range(queue_size):
                sp.next_track()  # Skip to the next track in the queue
                print("Skipped a track in the queue.")

        # Start playback with the first track in shuffled results
        track_to_play = shuffled_tracks[0]
        track_uri = track_to_play['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Playing: {track_to_play['name']} by {track_to_play['artists'][0]['name']}")

        # Queue the rest of the shuffled tracks
        track_uris = [track['uri'] for track in shuffled_tracks[1:]]
        for uri in track_uris:
            sp.add_to_queue(uri)  # Add each track to the queue individually
        print("Added more tracks to the queue from your search results.")

    else:
        print("No tracks found for your search.")
else:
    # If no song name is provided, check if there are previous search results
    if previous_search_results:
        # Shuffle the previous search results
        shuffled_tracks = random.sample(previous_search_results, len(previous_search_results))

        # Start playback with the first track in shuffled results
        track_to_play = shuffled_tracks[0]
        track_uri = track_to_play['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Playing a track from previous search: {track_to_play['name']} by {track_to_play['artists'][0]['name']}")

        # Queue the rest of the shuffled tracks
        track_uris = [track['uri'] for track in shuffled_tracks[1:]]
        for uri in track_uris:
            sp.add_to_queue(uri)  # Add each track to the queue individually
        print("Added more tracks to the queue from previous search results.")
    else:
        # Play related songs if there are no previous search results
        if current_playback and current_playback['is_playing']:
            # Get related tracks using recommendations
            seed_tracks = [track['id']]
            recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)

            if recommendations['tracks']:
                # Shuffle related tracks
                related_tracks = random.sample(recommendations['tracks'], len(recommendations['tracks']))

                # Start playback with the first related track
                first_related_track = related_tracks[0]
                sp.start_playback(uris=[first_related_track['uri']])
                print(f"Playing a related track: {first_related_track['name']} by {first_related_track['artists'][0]['name']}")

                # Queue the rest of the related tracks
                related_track_uris = [rec['uri'] for rec in related_tracks[1:]]
                for uri in related_track_uris:
                    sp.add_to_queue(uri)  # Add each related track to the queue
                print("Added more related tracks to the queue.")
            else:
                print("No related tracks found.")
        else:
            # Play a random track from a broader search if no song name is provided and no previous results exist
            random_results = sp.search(q='*', type='track', limit=50)  # Search for a wider range of tracks
            if random_results['tracks']['items']:
                random_track = random.choice(random_results['tracks']['items'])
                track_uri = random_track['uri']
                sp.start_playback(uris=[track_uri])
                print(f"Playing a random track: {random_track['name']} by {random_track['artists'][0]['name']}")
            else:
                print("No random tracks found.")
