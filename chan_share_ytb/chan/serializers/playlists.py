from chan.models import Playlist
from chan.serializers.base import BaseSerializer
from rest_framework.serializers import ModelSerializer

class PlaylistSerializer(BaseSerializer):

    class Meta:
        model = Playlist
        fields = [  'id',
                    'title',
                    'mode',
                    'created',
                    'updated']

class PlaylistCreateSerializer(ModelSerializer):

    class Meta:
        model = Playlist
        fields = ['title', 'mode']

    def __init__(self, *args, **kwargs):
        if 'mode' in kwargs.keys(): # add logic here for optional viewing
            self.Meta.fields = list(self.Meta.fields)
            self.Meta.fields.append(kwargs['mode'])
        super(PlaylistCreateSerializer, self).__init__(*args, **kwargs)
