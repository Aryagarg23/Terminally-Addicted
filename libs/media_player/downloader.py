import yt_dlp
import os
import shutil

def clear_folder(output_folder):
    """
    Deletes all files and subdirectories in the output folder.
    
    Args:
        output_folder (str): Path to the folder to be cleared.
    """
    if os.path.exists(output_folder):
        # Remove all files and subdirectories
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def download_media(youtube_url, output_folder="./buffer/media"):
    """
    Downloads a YouTube or X.com video in two formats:
    1. MP4 (video with audio, highest quality) - saved as 'buffer_video.mp4'
    2. MP3 (audio only) - saved as 'buffer_audio.mp3'
    
    Args:
        youtube_url (str): URL of the video to download.
        output_folder (str): Directory to save the files. Defaults to './buffer/media'.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        # Clear the folder before downloading
        clear_folder(output_folder)

    # Define specific file paths
    video_output_path = os.path.join(output_folder, "buffer_video.mp4")
    audio_output_path = os.path.join(output_folder, "buffer_audio")  # Don't change this please

    # Download the MP4 (highest quality video with audio)
    ydl_opts_video = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio
        'outtmpl': video_output_path,  # Save video with the specific name 'buffer_video.mp4'
        'merge_output_format': 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegVideoRemuxer',
                'preferedformat': 'mp4',
            },
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([youtube_url])
        print(f"MP4 (video with audio) download complete! Saved as {video_output_path}")
    except Exception as e:
        print(f"An error occurred while downloading video: {e}")

    # Download the MP3 (audio only)
    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': audio_output_path,  # Save audio with the specific name 'buffer_audio.mp3'
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([youtube_url])
        print(f"MP3 download and conversion complete! Saved as {audio_output_path}")
    except Exception as e:
        print(f"An error occurred while downloading audio: {e}")

import os
import yt_dlp

def save_link(youtube_url, output_path):
    """
    Downloads a YouTube or X.com video in the highest quality available (audio and video) 
    and saves it as a single MP4 file.

    Args:
        youtube_url (str): URL of the video to download.
        output_path (str): Full path (including filename) where the MP4 will be saved.
    """
    # Ensure the output folder exists
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Download the MP4 (highest quality video with audio)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio
        'outtmpl': output_path,  # Save video at the specified output path
        'merge_output_format': 'mp4',  # Merge video and audio into an mp4 file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"Download complete! Video saved as {output_path}")
    except Exception as e:
        print(f"An error occurred while downloading: {e}")
