from django.db import models
from auth_.models import CustomUser

class Course (models.Model):
    title = models.CharField(max_length=255, null=False,blank=False)
    description = models.TextField()
    created_at = models.DateTimeField (auto_now_add=True)

    def __str__(self):
        return self.title.__str__()

class Module (models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False,blank=False)
    sort_index = models.IntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.__str__()

class Chapter (models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.TextField()
    sort_index = models.IntegerField(db_index=True)
    is_signable = models.BooleanField(default=True)
    content_filepath = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title.__str__()

class CourseProgression (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    current_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    current_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    last_entry = models.DateTimeField(auto_now=True)

class CompletedSignable (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    word = models.CharField(max_length=255, null=False, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

class CompletedCourse (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
