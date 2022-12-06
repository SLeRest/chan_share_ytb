from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from chan.models import Song, Playlist 
from chan.serializers.playlists import PlaylistSerializer, PlaylistCreateSerializer

class PlaylistViewset(ModelViewSet):

    serializer_class = PlaylistSerializer
    # TODO faire reflechir aux droit des playlist (tres lier aux droits des song) 
    #permission_classes = [PLaylistPermission]
    # En phase de dev, on va pas se prendre la tete avec la permission
    permission_classes = [AllowAny]

    # TODO recuperer user id dans le jwt token voir comment faire
    def get_queryset(self):
        #return Playlist.objects.filer(user_id=get_username)
        return Playlist.objects.all()

    def create(self, request, *args, **kwargs):
        input_serializer = PlaylistCreateSerializer(data=request.data) 
        input_serializer.is_valid(raise_exception=True)
        self.perform_create(input_serializer)
        serializer = PlaylistSerializer(input_serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# CREATE TABLE IF NOT EXISTS "auth_user"(]
#     "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#     "password" varchar(128) NOT NULL,
#     "last_login" datetime NULL,
#     "is_superuser" bool NOT NULL,
#     "username" varchar(150) NOT NULL UNIQUE,
#     "last_name" varchar(150) NOT NULL,
#     "email" varchar(254) NOT NULL,
#     "is_staff" bool NOT NULL,
#     "is_active" bool NOT NULL,
#     "date_joined" datetime NOT NULL,
#     "first_name" varchar(150) NOT NULL
# );
