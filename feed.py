'''
# this part creates the the playlist of all my playlists

import os
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from datetime import timedelta
import isodate
import pandas as pd

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]





# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"


# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    return  googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

def get_playlist_ids(youtube):
    playlist_ids = []
    next_page_token = None

    while True:
        response = youtube.playlists().list(
            part="id",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            playlist_ids.append(item['id'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return playlist_ids

def get_all_videos_from_playlists(youtube, playlist_ids):
    all_video_ids = []

    for playlist_id in playlist_ids:
        next_page_token = None

        while True:
            response = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in response['items']:
                all_video_ids.append(item['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

    return all_video_ids

# Main
youtube = get_authenticated_service()
playlist_ids = get_playlist_ids(youtube)
all_video_ids = get_all_videos_from_playlists(youtube, playlist_ids)

#print(all_video_ids)


#for i in all_video_ids:
 #   print(i)

 #33983 number of video

unique_video_ids = list(set(all_video_ids))

with open("all_video_ids.txt", "w") as file:
    for video_id in unique_video_ids:
        file.write(video_id + "\n")

print("All video IDs have been saved to 'all_video_ids.txt'.")

'''


#--------------------importing all my playlists from youtube api, above-------------------------------------------------------------------

#this part get the list of today feed

from seleniumbase import Driver
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import time


'''
driver = Driver(uc=True)
driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&ec=65620&hl=en&ifkv=ARpgrqcIpJigo9VqlcGwGwHtRW99hkAqltAMDNwZrawjOFUOUwboM9bUOLfmT12Y7fcYHtWHSBFMAg&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1221043594%3A1728787304780556&ddm=0")
driver.type("#identifierId", "taboubacartoure93@gmail.com")
driver.click("#identifierNext > div > button")

driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", "Password")
driver.click("#passwordNext > div > button")
'''


driver = Driver(uc=True)
driver.get("https://www.youtube.com/results?search_query=scienceetonnante")



# Scroll down to load more results
# Define the number of times to scroll the page
scroll_count = 3

# Define the delay (in seconds) between each scroll
scroll_delay = 2

# Loop to perform scrolling
for _ in range(scroll_count):
    # Execute JavaScript to scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, 100000000);")
    
    # Pause for a moment to allow the content to load
    time.sleep(scroll_delay)


html =driver.get_page_source()
market_soup = soup(html, 'html.parser')

#markert_soup = market_soup.encode("utf-8")

# End the automated browsing session
driver.quit()


videos = {}

for link in market_soup.find_all('a', href=True, title=True):  # Assuming title is in <a> tag
    match = re.search(r'v=([a-zA-Z0-9_-]{11})', link['href'])
    if match:
        video_id = match.group(1)
        title = link['title']  # Get the title from the attribute
        videos[video_id] = title

with open("all_video_ids_from_search.txt", "w") as file:
    for video_id in videos:
        file.write(video_id + "\n")

print("All video IDs have been saved to 'all_video_ids_from_search.txt'.")



























