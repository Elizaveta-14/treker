from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from config import settings
from habit.apps import HabitConfig
from habit.views import HabitViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register("", HabitViewSet, basename="habit")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
