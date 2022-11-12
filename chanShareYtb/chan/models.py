from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Playlist(Base):
    title = models.CharField(max_length=255)
    mode = models.CharField(max_length=20) # TODO enum

    class Meta:
        ordering = ('created', )
        db_table = 'playlist'

class Song(Base):

    class DownloadStatus(models.TextChoices):
        DOWNLOAD = 'DL', _('Download')
        IN_QUEUE = 'IQ', _('In queue')
        FAILED = 'FL', _('Failed')
        SUSPEND = 'SP', _('Suspend')
        NOT_STARTED = 'NS', _('Not Started')

    title = models.CharField(max_length=255, null=True, default=None)
    title_ytb = models.CharField(max_length=255, null=True, default=None)
    channel_ytb = models.CharField(max_length=255, null=True, default=None)
    url_ytb = models.URLField()
    date = models.DateField(null=True, default=None)
    download_status = models.CharField(
        max_length=2,
        choices=DownloadStatus.choices,
        default=DownloadStatus.NOT_STARTED
    )

    class Meta:
        ordering = ('created', )
        db_table = 'song'

class PlaylistSongs(Base):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        db_table = 'playlist_songs'

class UserRelationship(Base):
    user_first_id = models.ForeignKey(User, related_name='first', on_delete=models.CASCADE)
    user_second_id = models.ForeignKey(User, related_name='second',  on_delete=models.CASCADE)
    pending_first_second = models.BooleanField(default=False)
    pending_second_first = models.BooleanField(default=False)
    refuse_first_second = models.BooleanField(default=False)
    refuse_second_first = models.BooleanField(default=False)
    friend = models.BooleanField(default=False)
    block_first_second = models.BooleanField(default=False)
    block_second_first = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_relationship'
