import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_youtube(keyword, api_key):
    # URL for the YouTube search endpoint
    url = "https://www.googleapis.com/youtube/v3/search"
    
    # Parameters for the search
    params = {
        'part': 'snippet',
        'q': keyword,
        'type': 'video',
        'maxResults': 5,
        'key': api_key
    }
    
    # Send a GET request to the YouTube API
    response = requests.get(url, params=params)
    
    # Check for successful response
    if response.status_code == 200:
        results = response.json()
        video_info = []
        
        # Extract video details from the results
        for item in results['items']:
            # Ensure that the item is a video
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                title = item['snippet']['title']
                author = item['snippet']['channelTitle']
                
                video_info.append({
                    'url': video_url,
                    'title': title,
                    'author': author
                })
        
        return video_info
    else:
        print("Error:", response.json())
        return []
