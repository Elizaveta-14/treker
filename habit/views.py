from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from habit.models import Habit
from habit.paginations import HabitPagination
from habit.permissions import IsOwner
from habit.serializer import HabitSerializer


class HabitViewSet(ModelViewSet):
    """ViewSet для модели HABIT"""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_permissions(self):
        """CRUD только для владельцев или Администратора"""

        if self.action == "create":
            self.permission_classes = (IsOwner | IsAdminUser,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsOwner | IsAdminUser,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | IsAdminUser,)
        return super().get_permissions()

    # def perform_create(self, serializer):
    #     """ Записываем авторизированного пользователя в обьект OWNER """
    #
    #     serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Переопределение вывода информации: если Админ то все, если пользователь то только с пометкой is_public"""

        if self.request.user.is_staff:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(is_public=True)
