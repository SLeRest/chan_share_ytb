import youtube_dl
from django.conf import settings

def download_ytb_mp3(url, id):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = url,download=False
    )
    filename = f"{settings.PATH_SONGS}/{id}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
