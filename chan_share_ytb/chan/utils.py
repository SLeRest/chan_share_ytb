from django.conf import settings
from django.core.files import File

import requests
import os
import shutil
import json
import yt_dlp
from datetime import timedelta, datetime
from pathlib import Path
from PIL import Image


def download_ytb_mp3(url):
    # TODO automatic log sur stdout dans youtubeDL
    # voir comment eviter ca
    video_info = yt_dlp.YoutubeDL({}).extract_info(url, download=False)
    # OK donc la on a plusieur possibilite
    # si _type est present -> check ce que c'est
    #       ca peut etre une playlist et dans ce cas la on loop
    #       ca peut etre autre chose
    path = f"{settings.DATA_SONGS_PATH}/{video_info['id']}.mp3"

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        #  See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    
    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     error_code = ydl.download(url)

    return video_info

def get_thumnnail_png(song, video_info):
    # Download thumbnail and put it in thumbnail dir
    r = requests.get(video_info['thumbnail'], stream = True)
    webp_path = f'{settings.DATA_THUMBNAILS_PATH}/{video_info["id"]}.webp'
    png_path = f'{settings.DATA_THUMBNAILS_PATH}/{video_info["id"]}.png'
    if r.status_code == 200:
        try:
            with open(webp_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        except Exception as e:
            raise e
    else:
        raise APIException(r.text)
    # Convert webp file to png file
    try:
        with Image.open(webp_path).convert("RGB") as im:
            im.save(png_path, "png")
    except Exception as e:
        raise APIException(r.text)
    # Delete webp Image
    try:
        os.remove(webp_path) # DEBUG vaut mieux mettre os. avant pour plus de clarte
    except OSError as e:  ## if failed, report it back to the user ##
        print (f'Error: {e.filename} - {e.strerror}')
    # Add image to BDD
    song.thumbnail.name = png_path
    return song

def create_song_from_video_info(song, video_info):
    song.id_ytb = video_info["id"]
    song.title = video_info["title"]
    song.channel_id = video_info["channel_id"]
    song.channel_url = video_info["channel_url"]
    song.channel_title = video_info["channel"]
    song.uploader_id = video_info["uploader_id"]
    song.uploader_name = video_info["uploader"]
    song.duration = timedelta(seconds=video_info["duration"])
    song.description = video_info["description"]
    song.upload_date = datetime.strptime(video_info["upload_date"], '%Y%m%d').date()
    for tag in video_info["tags"] : song.tags.add(tag) 
    song = get_thumnnail_png(song, video_info)
    # TODO send to the queue
    #song = get_song_mp3(song, video_info)
    song.save()
    return song
