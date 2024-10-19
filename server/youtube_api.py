import requests

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

# Replace 'YOUR_API_KEY' with your actual API key and 'YOUR_SEARCH_KEYWORD' with the keyword you want to search
api_key = 'key'
keyword = 'martin luther king'

video_results = search_youtube(keyword, api_key)

# Print the results
for video in video_results:
    print(f"Title: {video['title']}\nAuthor: {video['author']}\nURL: {video['url']}\n")
