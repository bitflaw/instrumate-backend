from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("upload/", views.HandleUpload.as_view(), name="upload"),
    path("media/<str:filename>/", views.ServeFiles.as_view(), name="serve_image"),
    path("translate/eng_to_ksl/", views.Eng_To_KSL.as_view(), name="eng_to_ksl"),
    path("translate/ksl_to_eng/", views.KSL_To_Eng.as_view(), name="ksl_to_eng"),
    path('serve_bvh/', views.ServeBvh.as_view(), name='serve_bvh'),
]
urlpatterns += static('/media', document_root='/tmp/upload_dir/images')
