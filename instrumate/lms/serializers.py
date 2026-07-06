from rest_framework import serializers
from . import models

class CourseSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'
        read_only_fields = ['created_at']


class ModuleSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = '__all__'
        read_only_fields = ['created_at']

class ChapterSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = '__all__'
        read_only_fields = ['created_at']

class CourseProgressionSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.CourseProgression
        fields = '__all__'
        read_only_fields = ['last_entry']
        depth = 1

class CompletedSignableSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.CompletedSignable
        fields = '__all__'
        read_only_fields = ['completed_at']

class CompletedCourseSerializer (serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = models.CompletedCourse
        fields = '__all__'
        read_only_fields = ['completed_at']
