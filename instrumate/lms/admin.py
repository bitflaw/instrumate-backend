from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.CourseProgression)
admin.site.register(models.CompletedCourse)
admin.site.register(models.Module)
admin.site.register(models.Chapter)
admin.site.register(models.CompletedSignable)
