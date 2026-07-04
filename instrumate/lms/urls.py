from rest_framework import routers, urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from . import views
import os

router = routers.SimpleRouter()

router.register(r'courses',           views.CourseViewSet)
router.register(r'modules',           views.ModuleViewSet)
router.register(r'chapters',          views.ChapterViewSet)
router.register(r'words',             views.CompletedSignableViewSet)
router.register(r'course_progress',   views.CourseProgressionViewSet)
router.register(r'completed_courses', views.CompletedCourseViewSet)

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(
            '/media/',
            document_root=os.path.join(settings.BASE_DIR, 'content')
        )
