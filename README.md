# StoryWizard

StoryWizard is a Python script that automates the process of downloading Instagram stories and uploading them to YouTube. It uses `instaloader` to fetch stories from Instagram and leverages the YouTube Data API to upload videos. This tool is useful for content creators, digital marketers, and anyone interested in automating their social media content management.

## Features

- **Instagram Story Download**: Automatically downloads new Instagram stories.
- **YouTube Video Upload**: Uploads the downloaded stories to YouTube.
- **Automated Workflow**: Runs continuously to check for new stories and upload them.
- **Custom YouTube Metadata**: Allows setting custom titles, descriptions, and other metadata for YouTube uploads.

## Requirements

- Python 3
- `instaloader`
- `google-api-python-client`
- `oauth2client`
- An Instagram account for downloading stories.
- A YouTube account for uploading videos.

## Setup

1. **Install Required Libraries**:
   ```bash
   pip install instaloader google-api-python-client oauth2client
   ```

2. **Google API Credentials**: You need to set up your OAuth 2.0 credentials on the Google Developer Console and download the `client_secret.json` file.

3. **Configure the Script**: Place your `client_secret.json` in the project directory and update the `CLIENT_SECRETS_FILE` path in the script.

4. **Instagram Credentials**: Update `ig_username` and `ig_password` with your Instagram credentials.

## Usage

1. Run the script:
   ```bash
   python storywizard.py
   ```

2. The script will log into Instagram, download new stories, and upload them to YouTube.

3. The script runs in a loop, continuously checking for new stories.

## Important Notes

- **Security**: Ensure your Instagram and YouTube credentials are secure.
- **API Limits**: Be aware of YouTube API's quota limits.
- **Privacy**: Respect the privacy of the content creators. Do not upload content without permission.

## Disclaimer

This tool is intended for educational purposes and should be used responsibly. The developers are not responsible for any misuse or violation of terms of service of the respective platforms.

---

For more information and updates, visit the [GitHub repository](https://github.com/darkwolfcreek/storywizard).
