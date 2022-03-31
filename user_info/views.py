from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import UserInfo
from .serializers import RegisterSerializer


class RegisterViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    注册接口
    """

    serializer_class = RegisterSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [AllowAny]