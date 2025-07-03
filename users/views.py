from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.permissions import IsUserProfile

from users.serializer import UserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny


class UserViewSet(ModelViewSet):
    """ViewSet для модели USER"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """ Хэширование пароля при создании """

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        """ CRUD только для владельцев или Администратора"""

        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsUserProfile | IsAdminUser,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()
