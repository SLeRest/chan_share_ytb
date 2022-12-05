from rest_framework.viewsets import ModelViewSet
from chan.serializers.users import UserSerializer
from django.contrib.auth.models import User

# ViewSets define the view behavior.
class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
