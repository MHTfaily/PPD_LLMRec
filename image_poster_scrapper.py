# # installing packages
# !pip install requests beautifulsoup4 pillow

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re

def search_movie_poster(movie_name):
    # Format the search query to include "high resolution movie poster"
    query = f"{movie_name} high resolution movie poster imdb"
    query = '+'.join(query.split())

    # Perform the search using Google Images
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    
    # Send HTTP GET request
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    if response.status_code == 200:
        # Parse the response content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first high-resolution image
        # Google Images stores links to images in data attributes
        images = soup.find_all('img')
        
        for img in images:
            img_url = img.get('data-src') or img.get('src')  # Check both 'data-src' and 'src'
            if img_url and re.match(r'^https?://', img_url):
                # Download the image
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    # Load image from memory for correctness and save to disk
                    image = Image.open(BytesIO(img_response.content))
                    image_path = f"{movie_name.replace(' ', '_')}_poster.jpg"
                    image.save(image_path)
                    print(f"Downloaded and saved {movie_name} poster in high resolution.")
                    return
    print("Failed to find a suitable high-resolution movie poster.")


# # Example of usage
# movie_name = "troy"
# search_movie_poster(movie_name)
