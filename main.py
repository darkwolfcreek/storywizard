import instaloader
import os
import time
import sys
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import json

CLIENT_SECRETS_FILE = "C:/Users/guam/PycharmProjects/pythonProject/client_secret_951312463896-4qklnuhmvvst1gvp4e4kffql502usg8p.apps.googleusercontent.com.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

uploaded_videos_file = "uploaded_videos.json"
youtube_api_calls = 0
def get_authenticated_service():
    oauth2_file = "%s-oauth2.json" % sys.argv[0]

    if not os.path.exists(oauth2_file):
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
        storage = Storage(oauth2_file)
        credentials = run_flow(flow, storage, argparser.parse_args())
    else:
        storage = Storage(oauth2_file)
        credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
        credentials = run_flow(flow, storage, argparser.parse_args())

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

def upload_video(filename, title, description, category, keywords, privacyStatus, uploaded_videos_file, youtube_service):
    global youtube_api_calls  # Use the global counter

    if video_uploaded(filename, uploaded_videos_file):
        print(f"Video {filename} already uploaded.")
        return

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': keywords.split(","),
            'categoryId': category
        },
        'status': {
            'privacyStatus': privacyStatus
        }
    }

    insert_request = youtube_service.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )

    try:
        response = insert_request.execute()
        print(f"Video uploaded. Video ID: {response['id']}")
        mark_video_uploaded(filename, uploaded_videos_file)
    except HttpError as e:
        print(f"An HTTP error occurred: {e.resp.status} - {e.content}")
    finally:
        youtube_api_calls += 1  # Increment the API call counter after every attempt

def story_already_downloaded(dirname, item):
    expected_video_filename = os.path.join(dirname, f"{item.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.mp4")
    return os.path.exists(expected_video_filename)

def video_uploaded(filename, uploaded_videos_file):
    if not os.path.exists(uploaded_videos_file):
        return False
    with open(uploaded_videos_file, 'r') as file:
        uploaded_videos = json.load(file)
    return filename in uploaded_videos

def mark_video_uploaded(filename, uploaded_videos_file):
    uploaded_videos = []
    if os.path.exists(uploaded_videos_file):
        with open(uploaded_videos_file, 'r') as file:
            uploaded_videos = json.load(file)

    uploaded_videos.append(filename)

    with open(uploaded_videos_file, 'w') as file:
        json.dump(uploaded_videos, file, indent=4)

def print_loading_animation(current, total):
    progress = int((current / total) * 10)
    animation = "[{}{}]".format("■" * progress, "□" * (10 - progress))
    sys.stdout.write("\r" + animation)
    sys.stdout.flush()

def download_stories(username, L):
    print(f"Fetching profile of {username}...")
    profile = instaloader.Profile.from_username(L.context, username)

    dirname = f"{username}_stories"
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    print(f"Checking stories of {username}...")
    new_stories_downloaded = False
    story_items = L.get_stories(userids=[profile.userid])

    for story in story_items:
        for item in story.get_items():
            if item.is_video and not story_already_downloaded(dirname, item):
                print(f"\nDownloading video story: {item.date_utc}")
                L.download_storyitem(item, dirname)
                new_stories_downloaded = True

    if new_stories_downloaded:
        print("\nNew video stories downloaded.")
    else:
        print("\nNo new video stories to download.")
    return True

if __name__ == "__main__":
    username = "name"
    L = instaloader.Instaloader()
    ig_username = "name"
    ig_password = "pass"
    print("Logging in...")
    L.login(ig_username, ig_password)
    print("Logged in successfully.")

    if not os.path.exists(uploaded_videos_file):
        with open(uploaded_videos_file, 'w') as file:
            json.dump([], file, indent=4)

    youtube_service = get_authenticated_service()  # Get the YouTube service once outside the loop

    try:
        while True:
            new_videos = download_stories(username, L)

            if new_videos:
                dirname = f"{username}_stories"
                for file in os.listdir(dirname):
                    if file.endswith(".mp4"):
                        filepath = os.path.join(dirname, file)
                        upload_video(
                            filename=filepath,
                            title=f"Video from {username}",
                            description="Uploaded by InstaLoader Script",
                            category="22",
                            keywords="Instagram,Story,AutoUpload",
                            privacyStatus="private",
                            uploaded_videos_file=uploaded_videos_file,
                            youtube_service=youtube_service
                        )

            print(f"Waiting for the next check... YouTube API calls made so far: {youtube_api_calls}")
            time.sleep(60)

    except KeyboardInterrupt:
        print(f"\nApplication stopped. Total YouTube API calls made: {youtube_api_calls}")