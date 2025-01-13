import tweepy
import requests
import bs4
import os
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api
import time
from tqdm import tqdm
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

sys.stdout.reconfigure(encoding='utf-8')

used=set()
# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
)

client = tweepy.Client(
    bearer_token=os.getenv('BEARER_TOKEN'),
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)

def download_video(url, mention_id, user_screen_name, client):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
        download_dir = Path("downloads")
        download_dir.mkdir(exist_ok=True)
        download_path = f"downloads/video_{mention_id}.mp4"
        with open(download_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        print(f"Video downloaded successfully to {download_path}")
        response = cloudinary.uploader.upload(
            download_path,
            resource_type="video"
        )
        video_url = response['secure_url']
        downloadable_url = f"{video_url}?fl_attachment"
        client.create_tweet(
            text=f"@{user_screen_name} Please download video from the link: {downloadable_url}",
            in_reply_to_tweet_id=mention_id
        )
        os.remove(download_path)
        
    except Exception as e:
        print(f"Error downloading video: {e}")
        client.create_tweet(
            text=f"@{user_screen_name} Sorry, there was an error processing your video request.",
            in_reply_to_tweet_id=mention_id
        )

def extract_twitter_video_url(tweet_url, client):
    """Extract the highest quality video URL from a tweet."""
    try:
        api_url = f"https://twitsave.com/info?url={tweet_url}"
        response = requests.get(api_url)
        data = bs4.BeautifulSoup(response.text, "html.parser")
        download_button = data.find_all("div", class_="origin-top-right")[0]
        quality_buttons = download_button.find_all("a")
        return quality_buttons[0].get("href")
    except Exception as e:
        print(f"Error extracting video URL: {e}")
        return None

def process_mentions(client):
    """Process mentions and handle video downloading."""
    try:
        user_id = client.get_me().data.id
        
        mentions = client.get_users_mentions(
            user_id,
            max_results=5,
            tweet_fields=['referenced_tweets', 'author_id'],
            expansions=['author_id'],  # Include author info in the response
            user_fields=['username']   # Get username directly from mentions
        )

        if not mentions.data:
            print("No new mentions found.")
            return

        # Create a mapping of user IDs to usernames from the includes
        users = {user.id: user.username for user in mentions.includes['users']} if 'users' in mentions.includes else {}

        for mention in mentions.data:
            if mention.id in used:
                break
            used.add(mention.id)
            print(f"Processing mention ID: {mention.id}")
            
            # Get username from the mapping instead of making another API call
            user_screen_name = users.get(mention.author_id)
            print(f"Processing for user: {user_screen_name}")

            if mention.referenced_tweets:
                original_tweet_id = mention.referenced_tweets[0].id
                tweet_url = f"https://twitter.com/i/status/{original_tweet_id}"
                
                video_url = extract_twitter_video_url(tweet_url, client)
                if video_url:
                    download_video(video_url, mention.id, user_screen_name, client)
                else:
                    client.create_tweet(
                        text=f"@{user_screen_name} Sorry, I couldn't find a video in the tweet you replied to.",
                        in_reply_to_tweet_id=mention.id
                    )
            else:
                print("Mention is not a reply to a tweet")

    except Exception as e:
        print(f"Error processing mentions: {e}")

if __name__ == "__main__":
    # Set console to UTF-8 mode
    if sys.platform.startswith('win'):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    while True:
        process_mentions(client)
        time.sleep(30*60)