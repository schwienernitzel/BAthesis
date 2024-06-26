# @author: Felix Patryjas - https://github.com/schwienernitzel
# @date: 25-04-2024
# @title: Python-Script to scrape YouTube user comments
# @version: v3.2

# BEFORE YOU RUN THE SCRIPT:
# 1. Setup the YouTube-API in Google Cloud Console to obtain your API key.
# 2. Insert your API key below.
# 3. Insert your playlist ID below.
# 4. Check your output path, usually it's /content.
# 4. Run the script and check if everything works.

# NOTES:
# - Only tested in python notebooks (e.g. Google Collab), you can either copy the source code or download & save the file as .ipynb
# - If you receive Error 403: Forbidden, Google blocked your IP-address because you scraped too much data in a specific amount of time
# - Make sure that your playlist privacy status and each comment section are set to public, otherwise you may receive Error 403: Forbidden aswell

use_cuda=True 

import csv
import datetime
import json
import os
import re
import unicodedata
import sys

from urllib.request import urlopen
from time import sleep

api_key = os.getenv('APIKEY')

if not api_key:
    print("\033[91mERROR: No Google API-Key found in the current runtime! Aborting...\033[0m")
    sleep(2)
    sys.exit(1)

playlist_id = 'PLCZ5sr32Y45BQvfvDpM4OyEv1FkJ7M9_u' # Insert your playlist ID

def playlist_reader(api_key, playlist_id): # This reads the content of the playlist and fetches the video IDs.
  counter = 0
  sleep(1)

  print("Fetching playlist information...")
  url = 'https://www.googleapis.com/youtube/v3/playlists?key='+api_key+'&part=snippet&id='+playlist_id+''
  response = urlopen(url)
  playlist_info = json.loads(response.read())
  playlist_title = playlist_info['items'][0]['snippet']['title']
  sleep(1)

  print(f"Selected playlist: '{playlist_title}'")
  sleep(1)

  print("Extracting content data...")
  data = []
  url = 'https://www.googleapis.com/youtube/v3/playlistItems?key='+api_key+'&part=snippet&maxResults=50&playlistId='+playlist_id+''
  nextPageToken = None

  while True:
    if nextPageToken:
      request_url = f'{url}&pageToken={nextPageToken}'
    else:
      request_url = url

    response = urlopen(request_url)
    json_data = json.loads(response.read())

    for item in json_data['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        data.append({'video_id': video_id, 'video_title': video_title})
        counter = counter+1

    if 'nextPageToken' in json_data:
        nextPageToken = json_data['nextPageToken']
    else:
        break

  sleep(1)
  print(f"Process completed. Total videos: {counter}")
  return data

def comment_scraper(api_key, data): # This scrapes the user comments and saves the output into a common .csv file
  sleep(1)
  print("Starting comment scraping...")
  total = len(data)
  current = 0
  total_comments = 0
  string_to_file = 'comment_id\treplaycount\tlikecount\tdate\ttime\temojis\tcomment\n'

  for info in data:
    video_id = info['video_id']
    video_title = info['video_title']

    url = 'https://www.googleapis.com/youtube/v3/commentThreads?key='+api_key+'&textFormat=plainText&part=snippet,replies&videoId='+video_id+'&maxResults=100'
    raw_url = url
    last_nextPageToken = '-'
    comment_id = 1
    current = current+1
    sleep(1)
    print(f"Scraping comments for Video {current}/{total} - Title: {video_title} - ID: {video_id}")

    while (comment_id < 100000):
      response = urlopen(url)
      json_data = json.loads(response.read())

      for item in json_data['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment = re.sub('[\s]+', ' ', comment)
        date = item['snippet']['topLevelComment']['snippet']['publishedAt']
        time = re.sub('.*T(\d\d:\d\d):\d\dZ', r'\1', date)
        date = re.sub('T.*', '', date)
        likecount = item['snippet']['topLevelComment']['snippet']['likeCount']
        replycount = item['snippet']['totalReplyCount']
        emojis = re.sub('[^\u263a-\U0001f645 \U00010000-\U0010ffff]', '', comment)
        emojis = re.sub(' ', '', emojis)
        string_to_file += str(comment_id)+'\t'+str(replycount)+'\t'+str(likecount)+'\t'+date+'\t'+time+'\t'+emojis+'\t'+comment+'\n'
        comment_id += 1
        total_comments += 1

      if 'nextPageToken' in json_data:
        nextPageToken = json_data['nextPageToken']
        url = raw_url + '&pageToken='+nextPageToken

      if (nextPageToken == last_nextPageToken):
            break

      last_nextPageToken = nextPageToken

  string_to_file = string_to_file.strip()
  with open('/content/raw.csv', 'w') as writefile:
      writefile.write(string_to_file)
  print("Done! File saved as 'raw.csv'.")
  sleep(2)
  print(f"Comment scraping completed. Total raw comments: {total_comments}")

youtube_ids = playlist_reader(api_key, playlist_id)
comment_scraper(api_key, youtube_ids)