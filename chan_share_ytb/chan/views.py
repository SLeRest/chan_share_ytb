from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from chan.models import Song 
from chan.permissions import SongPermission
from chan.serializers import SongSerializer, SongCreateSerializer
from chan.utils import download_ytb_mp3
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

    # TODO
    # faire une reponse avant la fin du download en disant que c'est dans la queue
    # on peut faire une request sur un endpoint status pour voir comment ca se passe
    def create(self, request):
        s = Song(request['url_ytb'])
        try:
            download_ytb_mp3(s.url_ytb, id)
        except Exception as e:
            msg = f'Error download: {str(e)}'
            raise APIException(status_code=500, default_detail=msg)
        return Response()

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
