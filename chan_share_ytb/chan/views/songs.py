from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.files import File

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from chan.models import Song 
#from chan.permissions import SongPermission
from chan.serializers.songs import SongSerializer, SongCreateSerializer
from chan.utils import create_song_from_video_info, download_ytb_mp3

# Create your views here.

# TODO faire une url "all" pour l'admin pour request tout les son
class SongViewset(ModelViewSet):

    serializer_class = SongSerializer
    # TODO faire reflechir aux droit des song (tres lier aux droits des playlist) 
    #permission_classes = [SongPermission]
     # En phase de dev, on va pas se prendre la tete avec la permission
    permission_classes = [AllowAny]
    # permission_classes = [
    #         IsAuthenticated, # TODO Check si user authentifier
    #         IsOwnerSong, # TODO check si c'est le creater / owner du son
    #         IsPublicSong, # TODO check si le son est en partage public
    #         # IsPublicFriendSong, # TODO check si c'est un son en public que avec amis 
    #         # IsFriendOwnerSong, # TODO check si user est un amis du owner
    #         # IsPublicGroupOwnerSong,TODO check si c'est un son en public sur un ou des groupe
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
    # TODO faut split cette fonction en plusieur c'est inbuvable
    # TODO NEXT VERSION
    # add Song to queue
    # la queue sera un autre programme dans un autre process python
    # dans le meme container docker
    # la queue se chargera de DL les son qui se trouve dans la file d'attente
    # et de changer le status_download dans la BDD
    # TODO
    # change status in Download
    # download
    # change status in Done

    def create(self, request):
        # Check si le son est deja present dans la BDD
        song = Song.objects.filter(url_ytb=request.data['url_ytb'])
        if song.count() > 0:
            # Le son est present
            # TODO check si le status du download du son
            # si le status est pas done faut re-try de dl le son
            serializer = SongSerializer(song.first())
            return Response(serializer.data)
        # si il n'est pas present on va l'ajouter
        song = Song(url_ytb=request.data['url_ytb'])
        song.save()
        # On test le download
        try:
            video_info = download_ytb_mp3(request.data['url_ytb'])
        except Exception as e:
            # TODO raise des exception specifique
            # pas uniquement 404, youtube peut etre down par exemple
            raise APIException(str(e))
        song = create_song_from_video_info(song, video_info)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=201)

    # donc django est un framework de m****, si on delete une row avec une image dedans
    # eeeeet baaaaah ca delete pas l'image (why ...)
    # Obliger de le faire a la mano ducoup
    # fastapi / SQLAlchemy BEST
    # test
    def destroy(self, request, *args, **kwargs):
        # Delete song in BDD
        try:
            song = Song.objects.get(id=kwargs['pk'])
            song.delete()
        except:
            pass
        # Delete thumbnail
        try:
            png_path = f"{settings.DATA_THUMBNAILS_PATH}/{kwargs['pk']}.png"
            os.remove(png_path)
        except:
            pass
        return Response(status=204)
