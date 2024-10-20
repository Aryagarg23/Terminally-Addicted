import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os
from dotenv import load_dotenv
load_dotenv()

def initialize_spotify_client():
    """Initialize the Spotify client using loaded credentials."""
    client_id = os.getenv('SPOTIPY_CLIENT_ID', '')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET', '')

    if not client_id or not client_secret:
        raise ValueError("Please set the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in the text file.")

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing"
    ))

SP = initialize_spotify_client()
def display_current_playback(sp = SP):
    """Display currently playing track information."""
    current_playback = sp.current_playback()
    if current_playback is not None and current_playback['is_playing']:
        track = current_playback['item']
        
        returnstring = (f"Currently playing: {track['name']} by {track['artists'][0]['name']}")
        return returnstring
    else:
        returnstring = ("No track is currently playing.")
        return returnstring

def change_song(song_name, sp=SP):
    """Change the currently playing song based on user input or play a random track."""
    current_playback = sp.current_playback()['item']['id']

    if song_name:
        results = sp.search(q=song_name, type='track', limit=20)
        
        if results['tracks']['items']:
            previous_search_results = results['tracks']['items']  # Update previous search results

            # Shuffle the search results
            shuffled_tracks = random.sample(previous_search_results, len(previous_search_results))

            # Clear the current queue
            clear_current_queue(sp)

            # Start playback with the first track in shuffled results
            play_track(shuffled_tracks[0])
            queue_tracks(shuffled_tracks[1:])

        else:
            print("No tracks found for your search.")
    else:
        if previous_search_results:
            # Shuffle previous search results
            shuffled_tracks = random.sample(previous_search_results, len(previous_search_results))
            play_track(shuffled_tracks[0])
            queue_tracks(shuffled_tracks[1:])
        else:
            play_related_tracks(current_playback)

def clear_current_queue(sp=SP):
    """Clear the current queue by skipping tracks."""
    current_playback = sp.current_playback()
    if current_playback and current_playback.get('context'):
        queue_size = current_playback.get('queue_length', 0)

        for _ in range(queue_size):
            sp.next_track()  # Skip to the next track in the queue
            return("Skipped a track in the queue.")
        return f"Current queue size: {queue_size}"
    
def play(sp = SP):
    sp.start_playback()

def pause(sp = SP):
    SP.pause_playback()
    
def next_track(sp = SP):
    sp.next_track()

def previous_track(sp = SP):
    SP.previous_track()

def play_track(track, sp=SP):
    """Start playback of a specified track."""
    track_uri = track['uri']
    sp.start_playback(uris=[track_uri])

def queue_tracks(tracks, sp=SP):
    """Queue additional tracks."""
    for track in tracks:
        sp.add_to_queue(track['uri'])  # Add each track to the queue individually

def play_related_tracks(current_playback, sp=SP):
    """Play related tracks based on the currently playing track."""
    if current_playback and current_playback['is_playing']:
        seed_tracks = [current_playback['item']['id']]
        recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)

        if recommendations['tracks']:
            related_tracks = random.sample(recommendations['tracks'], len(recommendations['tracks']))
            play_track(sp, related_tracks[0])
            queue_tracks(sp, related_tracks[1:])
        else:
            print("No related tracks found.")
    else:
        play_random_track()

def play_random_track(sp=SP):
    """Play a random track if no song name is provided and no previous results exist."""
    random_results = sp.search(q='*', type='track', limit=50)  # Search for a wider range of tracks
    if random_results['tracks']['items']:
        random_track = random.choice(random_results['tracks']['items'])
        play_track(sp, random_track)
    else:
        print("No random tracks found.")

