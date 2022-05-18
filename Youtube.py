import os
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def upload_video(chapter):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "Youtube_Credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": chapter.description,
                "title": chapter.title,
            },
            "status": {"privacyStatus": "private"},
        },
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(chapter.video_file_name),
    )
    response = request.execute()
    print("response: " + str(response))
    time.sleep(100)

    thumbnail_request = youtube.thumbnails().set(
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        videoId=response.get('id'),
        media_body=MediaFileUpload(chapter.thumbnail_file_name)
    )
    thumbnail_response = thumbnail_request.execute()
    print("thumbnail response: " + str(thumbnail_response))
    time.sleep(100)
