#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def get_audio_metadata(file_path):
    """Extract metadata from audio file."""
    audio = MP3(file_path, ID3=EasyID3)
    title = audio.get('title', [os.path.splitext(os.path.basename(file_path))[0]])[0]
    artist = audio.get('artist', ['Unknown'])[0]
    album = audio.get('album', ['Unknown'])[0]
    duration = int(audio.info.length)
    return {
        'title': title,
        'artist': artist,
        'album': album,
        'duration': duration
    }

def generate_feed(subfolder_path, repo_owner, repo_name):
    """Generate RSS feed for the subfolder."""
    config_path = os.path.join(subfolder_path, 'config.json')
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    podcast_title = config.get('title', 'Podcast')
    podcast_description = config.get('description', 'A podcast')
    podcast_link = config.get('link', 'https://example.com')
    podcast_language = config.get('language', 'en-us')
    podcast_author = config.get('author', 'Unknown')

    rss = Element('rss', version='2.0', attrib={'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})
    channel = SubElement(rss, 'channel')

    SubElement(channel, 'title').text = podcast_title
    SubElement(channel, 'description').text = podcast_description
    SubElement(channel, 'link').text = podcast_link
    SubElement(channel, 'language').text = podcast_language
    SubElement(channel, 'itunes:author').text = podcast_author
    SubElement(channel, 'itunes:summary').text = podcast_description

    # Find audio files
    audio_files = [f for f in os.listdir(subfolder_path) if f.endswith(('.mp3', '.m4a', '.wav'))]
    audio_files.sort()  # Sort by name, assuming chronological

    for audio_file in audio_files:
        file_path = os.path.join(subfolder_path, audio_file)
        metadata = get_audio_metadata(file_path)
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = metadata['title']
        SubElement(item, 'description').text = metadata.get('description', metadata['title'])
        SubElement(item, 'itunes:summary').text = metadata.get('description', metadata['title'])
        SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')  # Placeholder, use file mtime
        SubElement(item, 'enclosure', url=f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{subfolder_path}/{audio_file}', type='audio/mpeg', length=str(os.path.getsize(file_path)))
        SubElement(item, 'itunes:duration').text = str(metadata['duration'])

    # Pretty print XML
    rough_string = tostring(rss, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent='  ')

    feed_path = os.path.join(subfolder_path, 'feed.xml')
    with open(feed_path, 'w') as f:
        f.write(pretty_xml)
    print(f"Generated feed: {feed_path}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python generate_feed.py <subfolder> <repo_owner> <repo_name>")
        sys.exit(1)
    subfolder = sys.argv[1]
    repo_owner = sys.argv[2]
    repo_name = sys.argv[3]
    generate_feed(subfolder, repo_owner, repo_name)