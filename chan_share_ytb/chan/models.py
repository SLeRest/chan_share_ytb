from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from taggit.managers import TaggableManager

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# TODO
# reflechir aux liens entre playlist et user sur les droits
class Playlist(Base):

    class RightMode(models.TextChoices):
        PUBLIC = 'PB', _('Public')
        FRIEND = 'FR', _('Friend')
        GROUP = 'GR', _('Group')
        PERSONNAL = 'PN', _('Personnal')
        PRIVATE = 'PV', _('Private')

    title = models.CharField(max_length=255)
    mode = models.CharField(
        max_length=2,
        choices=RightMode.choices,
        default=RightMode.PUBLIC
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(
            Group,
            on_delete=models.SET_NULL,
            null=True,
            default=None
    )

    class Meta:
        ordering = ('created', )
        db_table = 'playlist'

# TODO faire un model de log de changement de status sur Song
class Song(Base):

    class DownloadStatus(models.TextChoices):
        DONE = 'DN', _('Done')
        DOWNLOAD = 'DL', _('Download')
        IN_QUEUE = 'IQ', _('In queue')
        FAILED = 'FL', _('Failed')
        SUSPEND = 'SP', _('Suspend')
        NOT_STARTED = 'NS', _('Not Started')

    id_ytb = models.CharField(max_length=255, null=True, default=None)
    url_ytb = models.URLField(max_length=200, unique=True)
    title = models.CharField(max_length=255, null=True, default=None)
    channel_id = models.CharField(max_length=255, null=True, default=None)
    channel_url = models.URLField(max_length=200, null=True, default=None)
    channel_title = models.CharField(max_length=255, null=True, default=None)
    uploader_id = models.CharField(max_length=255, null=True, default=None)
    uploader_name = models.CharField(max_length=255, null=True, default=None)
    duration = models.DurationField(null=True, default=None)
    tags = TaggableManager() # TODO type tag, voir la lib taggit et son fonctionnement
     # TODO type image, voir si on met une height et width fixe, il faut avoir la lib pillow askip
    thumbnail = models.ImageField(upload_to=settings.DATA_THUMBNAILS_PATH)
    description = models.TextField()
    upload_date_ytb = models.DateField(null=True, default=None) # Date de l'upload sur youtube
    download_datetime = models.DateField(null=True, default=None)
    download_error = models.TextField()
    #song = FileField(upload_to=settings.DATA_SONG_PATH, storage=None, max_length=100, **options)
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
