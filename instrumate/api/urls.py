from django.urls import path
from django.conf.urls.static import static
from . import views
import tempfile
import os

urlpatterns = [
    path ("upload/", views.HandleUpload.as_view(), name="upload"),
    path ("media/<str:filename>/", views.ServeFiles.as_view(), name="serve_image"),
    path ("translate/eng_to_ksl/", views.Eng_To_KSL.as_view(), name="eng_to_ksl"),
    path ("translate/ksl_to_eng/", views.KSL_To_Eng.as_view(), name="ksl_to_eng"),
    path ("get_animations/", views.Animations.as_view(), name="get_animation_data"),
]

tmp_dir = tempfile.gettempdir()
urlpatterns += static('/media', document_root=os.path.join(tmp_dir, '/upload_dir/images'))
