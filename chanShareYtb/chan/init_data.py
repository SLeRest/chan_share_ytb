from chan.models import Song
from django.db import models
import youtube_dl
from datetime import datetime, timedelta

# CMD
# python manage.py shell < chan/init_data.py 

# POST avec juste un url
url = 'https://www.youtube.com/watch?v=dFzJ4UPNL1w'

# On ajoute song dans la BDD avec le status (par default) not started
s = Song(url_ytb=url)
s.save()

# On test le download
video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
print(f'id: {video_info["id"]}')
print(f'title: {video_info["title"]}')
print(f'channel_id: {video_info["channel_id"]}')
print(f'channel_url: {video_info["channel_url"]}')
print(f'channel_title: {video_info["channel"]}')
print(f'uploader_id: {video_info["uploader_id"]}')
print(f'uploader: {video_info["uploader"]}')
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
s.uploader = video_info["uploader_name"]
s.duration = timedelta(seconds=video_info["duration"])
s.tags = video_info["tags"] # TODO a revoir apres avoir capter comment fonctionne taggit
 # TODO download image via l'url > voir comment on ajoute ? on met un f = open() ?
s.thumbnais = video_info["thumbnail"]
s.description = video_info["description"]
s.upload_date = datetime.strptime(video_info["upload_date"], '%Y%m%d').date()
s.save()
