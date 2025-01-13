# Twitter Video Downloader Bot

A Twitter bot that automatically downloads and provides downloadable links for videos from tweets when mentioned. The bot processes mentions, extracts video URLs from referenced tweets, uploads them to Cloudinary, and replies with a downloadable link.

## Features

- Monitors Twitter mentions every 30 minutes
- Downloads videos from referenced tweets
- Uploads videos to Cloudinary for secure storage
- Provides direct download links to users
- Handles error cases gracefully with user notifications
- Supports progress tracking for video downloads
- UTF-8 encoding support for international characters

## Prerequisites

- Python 3.6 or higher
- Twitter Developer Account with Elevated access
- Cloudinary Account

## Required Python Packages

```
tweepy
requests
beautifulsoup4
python-dotenv
tqdm
cloudinary
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd twitter-video-downloader-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following credentials:

```env
# Twitter API Credentials
BEARER_TOKEN=your_bearer_token
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret

# Cloudinary Credentials
CLOUD_NAME=your_cloud_name
API_KEY=your_api_key
API_SECRET=your_api_secret
```

## Usage

1. Start the bot:
```bash
python PyBot.py
```

2. To use the bot:
   - Find a tweet containing a video
   - Reply to that tweet mentioning the bot
   - The bot will process your mention and reply with a downloadable link

## How It Works

1. The bot checks for new mentions every 30 minutes
2. When mentioned in a reply to a tweet containing a video:
   - Extracts the video URL using twitsave.com
   - Downloads the video locally
   - Uploads the video to Cloudinary
   - Replies with a downloadable link
   - Cleans up local storage
3. Error handling:
   - If video extraction fails: Notifies the user
   - If download/upload fails: Sends an error message
   - Maintains UTF-8 encoding for international character support

## Technical Details

- Uses Tweepy for Twitter API interaction
- Implements rate limiting and pagination for Twitter API compliance
- Temporary files are stored in a `downloads` directory and cleaned up after processing
- Progress bars for video downloads using tqdm
- Automatic UTF-8 encoding configuration for Windows systems

## Limitations

- Can only process videos from public tweets
- Limited to Twitter's API rate limits
- Maximum video size determined by Cloudinary plan limits
- Processes up to 5 most recent mentions per check

## Error Handling

The bot handles several types of errors:
- Network connectivity issues
- Video extraction failures
- Download/upload problems
- API rate limiting
- Invalid video URLs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
