import sys
import logging
import requests
from pathlib import Path

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from chan.models import Song 
from chan.permissions import SongPermission
from chan.serializers import SongSerializer, SongCreateSerializer
from chan.utils import download_ytb_mp3

import youtube_dl
# Create your views here.

# TODO faire une url "all" pour l'admin pour request tout les son
class SongViewset(ModelViewSet):

    serializer_class = SongSerializer
    permission_classes = [SongPermission]
    # permission_classes = [
    #         IsAuthenticated, # TODO Check si user authentifier
    #         IsOwnerSong, # TODO check si c'est le creater / owner du son
    #         IsPublicSong, # TODO check si le son est en partage public
    #         # IsPublicFriendSong, # TODO check si c'est un son en public que avec amis 
    #         # IsFriendOwnerSong, # TODO check si user est un amis du owner
    #         # IsPublicGroupOwnerSong, # TODO check si c'est un son en public sur un ou des groupe
    #         # IsGroupOwnerSong, # TODO check si le user est dans un de ces groupes
    #         ]

    def get_queryset(self):
        # if self.action == "list":
        #     return Song.objects.filter(channel.owner.id == user.id)
        return Song.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return SongCreateSerializer # TODO
        return super().get_serializer_class()

    # TODO NEXT VERSION
    # faire une reponse avant la fin du download en disant que c'est dans la queue
    # on peut faire une request sur un endpoint status pour voir comment ca se passe
    # TODO
    # la on fait des print pour chaque erreur car on est en dev mode mais
    # faudrait une table dans la bdd pour les logs error
    def create(self, request):
        # Check si le son est deja present dans la BDD
        song = Song.objects.filter(url_ytb=request.data["url_ytb"])
        if song.count() > 0:
            # Le son est present
            serializer = SongSerializer(song.first())
            return Response(serializer.data)
        # si il n'est pas present on va l'ajouter
        song = Song(url_ytb=request.data["url_ytb"])
        song.save()
        print(f'Song saved: {song.title}')

        # On test le download
        try:
            video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
            print("Video data Ok")
        except Exception as e:
            # TODO raise des exception specifique
            # pas uniquement 404, youtube peut etre down par exemple
            raise APIException(status_code='404', detail=str(e))

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
        for tag in video_info["tags"] : s.tags.add(tag) 

        # Download thumbnail and put it in songs_data dir
        r = requests.get(video_info['thumbnail'], stream = True)
        if r.status_code == 200:
            p = f'{settings.DATA_SONG_PATH}/{video_info["id"]}.webp'
            with open(p, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print("Image downloaded")
        else:
            print(f'Failed download: {r.status_code}: {r.text}')
            raise APIException(status_code='500', detail=r.text)

        # Convert webp file to png file
        try:
            with Image.open(p).convert("RGB") as im:
                p = f'{settings.DATA_SONG_PATH}/{video_info["id"]}.png'
            im.save(p, "png")
            print(f'Image converted to png: {p}')
        except Exception as e:
            print(f'Error convert webp to png: {str(e)}')
            raise APIException(status_code='500', detail=r.text)

        # Add image to BDD
        p = Path(p)
        with path.open(mode='rb') as f:
            s.thumbnail = File(f, name=p.name)
            s.save()
        serializer = SongSerializer(song)
        return Response(serializer.data)

    # @action(detail=True, methods=['post'])
    # def download(self, request, id):
    #
    # @action(detail=True, methods=['get'])
    # def status(self, request, id):
    #     s = Song.objects.get(id=id)
    #     return Response(s.download_status)

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset that provides the standard actions
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     @action(detail=True, methods=['post'])
#     def set_password(self, request, pk=None):
#         user = self.get_object()
#         serializer = PasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user.set_password(serializer.validated_data['password'])
#             user.save()
#             return Response({'status': 'password set'})
#         else:
#             return Response(serializer.errors,
#                     status=status.HTTP_400_BAD_REQUEST)
#
#     @action(detail=False)
#     def recent_users(self, request):
#         recent_users = User.objects.all().order_by('-last_login')
#
#         page = self.paginate_queryset(recent_users)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(recent_users, many=True)
#         return Response(serializer.data)
