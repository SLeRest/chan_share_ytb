from django.urls import include, re_path
from rest_framework import routers

from chan.views.songs import SongViewset
from chan.views.playlists import PlaylistViewset
from chan.views.users import UserViewset

router = routers.SimpleRouter()
router.register(r'users', UserViewset, basename='user')
router.register(r'songs', SongViewset, basename='song')
router.register(r'playlists', PlaylistViewset, basename='playlist')

urlpatterns = [
    re_path(r'chan-share-ytb/api/0.0/', include(router.urls)),
]
