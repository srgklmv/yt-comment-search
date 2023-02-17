from configparser import *
from os import listdir
import requests


def check_api_key():
    if 'config.ini' not in listdir():
        yt_api_key = input('Enter your YT API key: ')
        config = ConfigParser()
        config['YOUTUBE'] = {'yt_api_key': yt_api_key}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


def get_comments(video_id, next_page_token=None, comments=[]):
    try:
        config = ConfigParser()
        config.read('config.ini')
        key = config['YOUTUBE']['yt_api_key']

        params = {
            'part': 'id,snippet,replies',
            'maxResults': 100,
            'videoId': video_id,
            'key': key
        }

        if next_page_token:
            params['pageToken'] = next_page_token

        response_json = requests.get('https://www.googleapis.com/youtube/v3/commentThreads', params).json()

        for item in response_json['items']:
            comment = item['snippet']['topLevelComment']
            text = comment['snippet']['textDisplay']
            comments.append(text)

        print('Parsing comments...')

    except Exception('Something goes wrong.'):
        pass
    else:
        if 'nextPageToken' in response_json:
            return get_comments(
                video_id,
                response_json['nextPageToken'],
                comments
            )
        else:
            return comments


def search_in_comments(sequence, comments):
    for comment in comments:
        if sequence.lower() in comment.lower():
            print(comment)


def main():
    check_api_key()
    sequence = input('Type in the word you are looking for: ')
    video = input('Enter video id: ')
    search_in_comments(sequence, get_comments(video))


if __name__ == '__main__':
    main()
