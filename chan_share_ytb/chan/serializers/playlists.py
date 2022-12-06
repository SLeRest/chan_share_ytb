from chan.models import Playlist
from chan.serializers.base import BaseSerializer
from rest_framework.serializers import ModelSerializer

class PlaylistSerializer(BaseSerializer):

    class Meta:
        model = Playlist
        fields = [  'id',
                    'title',
                    'mode',
                    'user',
                    'created',
                    'updated']

class PlaylistCreateSerializer(ModelSerializer):

    class Meta:
        model = Playlist
        fields = ['title', 'user']

    def __init__(self, *args, **kwargs):
        self.Meta.fields = list(self.Meta.fields)
        if 'mode' in kwargs.keys():
            self.Meta.fields.append(kwargs['mode'])
        if 'group' in kwargs.keys():
            self.Meta.fields.append(kwargs['group'])
        super(PlaylistCreateSerializer, self).__init__(*args, **kwargs)
