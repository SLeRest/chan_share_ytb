from chan.models import Song
from pathlib import Path
from PIL import Image
from django.core.files import File
from django.db.utils import IntegrityError
import requests
import sys
import youtube_dl
import shutil
from datetime import datetime, timedelta

# CMD
# python manage.py shell < chan/init_data.py 

# POST avec juste un url
url = 'https://www.youtube.com/watch?v=dFzJ4UPNL1w'

# On ajoute song dans la BDD avec le status (par default) not started
try:
    s = Song(url_ytb=url)
    s.save()
except IntegrityError:
    # La song est deja presente
    print("Song already here")
    sys.exit(0)

# On test le download
video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
print(f'id: {video_info["id"]}')
print(f'title: {video_info["title"]}')
print(f'channel_id: {video_info["channel_id"]}')
print(f'channel_url: {video_info["channel_url"]}')
print(f'channel_title: {video_info["channel"]}')
print(f'uploader_id: {video_info["uploader_id"]}')
print(f'uploader_name: {video_info["uploader"]}')
duration = timedelta(seconds=video_info["duration"])
print(f'duration: {duration}')
print(f'tags: {video_info["tags"]}')
print(f'thumbnais: {video_info["thumbnail"]}')
print(f'description: {video_info["description"]}')
upload_date = datetime.strptime(video_info["upload_date"], '%Y%m%d').date()
print(f'upload_date: {upload_date}') # TODO  a convertir en date python


s.id_ytb = video_info["id"]
s.title = video_info["title"]
s.channel_id = video_info["channel_id"]
s.channel_url = video_info["channel_url"]
s.channel_title = video_info["channel"]
s.uploader_id = video_info["uploader_id"]
s.uploader_name = video_info["uploader"]
s.duration = timedelta(seconds=video_info["duration"])
s.description = video_info["description"]
s.upload_date = datetime.strptime(video_info["upload_date"], '%Y%m%d').date()
for tag in video_info["tags"]:
    s.tags.add(tag) # TODO a revoir apres avoir capter comment fonctionne taggit

# Download file
r = requests.get(video_info['thumbnail'], stream = True)
if r.status_code == 200:
    p = f'/home/ouralgan/chan_share_ytb/chan_share_ytb/data_songs/{video_info["id"]}.webp'
    with open(p, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print("Image downloaded")
else:
    print(f'Failed download: {r.status_code}')
    print(r.text)
    sys.exit(1)
# Convert webp file to png file
try:
    with Image.open(p).convert("RGB") as im:
        p = f'/home/ouralgan/chan_share_ytb/chan_share_ytb/data_songs/{video_info["id"]}.png'
        im.save(p, "png")
    print(f'Image converted to png: {p}')
except Exception as e:
    print(f'Error convert webp to png: {str(e)}')
    sys.exit(2)
# Add image to BDD
path = Path(p)
with path.open(mode='rb') as f:
    s.thumbnail = File(f, name=path.name)
    s.save()
