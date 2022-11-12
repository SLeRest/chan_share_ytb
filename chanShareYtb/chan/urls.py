from django.urls import include, re_path
from rest_framework import routers

from chan import views

router = routers.SimpleRouter()
router.register(r'songs', views.SongViewset, basename='song')

urlpatterns = [
    re_path(r'chan-share-ytb/api/0.0/', include(router.urls)),
]
