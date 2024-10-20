import os
import threading
import signal
import subprocess
from pydub import AudioSegment
from pydub.playback import play

def play_video_and_audio():
    """
    Function to play a video (handled by a Go program) and audio (MP3).
    Video is played using 'go run main.go', and audio is played using pydub.
    The video and audio files are expected to be named 'buffer_video.mp4' and 'buffer_audio.mp3',
    located in the './buffer/media/' directory.
    """
    video_path = "./buffer/media/buffer_video.mp4"
    audio_path = audio_path = os.path.join(os.getcwd(), "buffer", "media", "buffer_audio.mp3")
    # Get the Python script's PID
    python_pid = os.getpid()
    print(f"Python script PID: {python_pid}")

    # Create an Event to signal when to start the audio
    audio_started_event = threading.Event()

    def play_audio(mp3_path):
        """
        Function to play the MP3 file using pydub.
        """
        try:
            # Wait until the signal handler signals that it has started
            print("Waiting for signal to start audio...")
            audio_started_event.wait()  # Wait until the event is set

            # Load the MP3 file
            audio = AudioSegment.from_mp3(mp3_path)
            # Play the audio
            print(f"Playing audio: {mp3_path}")
            play(audio)
            print("Audio finished playing.")
        except Exception as e:
            print(f"Error playing audio: {e}")

    def run_video_thread(video_path, python_pid):
        """
        Function to run the Go program with the video file.
        """
        # Save the current working directory to restore later
        original_dir = os.getcwd()
        
        try:
            # Change directory to where the Go file is located
            os.chdir("libs/pot")
            print(f"Running: go run main.go {video_path} {python_pid}")

            # Run the Go program with the video file as an argument
            cmd = ["go", "run", "main.go", f"../../{video_path}", str(python_pid)]
            subprocess.run(cmd)
            print("Video playback finished.")
        except Exception as e:
            print(f"Error running video: {e}")
        finally:
            # Change back to the original directory
            os.chdir(original_dir)

    # Set up the signal handler in the main thread
    def signal_handler(signum, frame):
        print(f"Signal received: {signum}")
        if signum == signal.SIGUSR1:
            print("SIGUSR1 received. Starting audio...")
            audio_started_event.set()

    signal.signal(signal.SIGUSR1, signal_handler)

    # Create threads for video and audio
    video_thread = threading.Thread(target=run_video_thread, args=(video_path, python_pid))
    audio_thread = threading.Thread(target=play_audio, args=(audio_path,))

    # Start both threads
    video_thread.start()
    audio_thread.start()

    # Wait for both threads to complete
    video_thread.join()
    audio_thread.join()

    print("Both video and audio playback finished.")
play_video_and_audio()
