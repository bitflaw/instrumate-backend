import os
import csv
from django.conf import settings
from rest_framework import status
from . import models, serializers
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CourseViewSet (viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated,]


class ModuleViewSet (viewsets.ModelViewSet):

    queryset = models.Module.objects.all()
    serializer_class = serializers.ModuleSerializer
    permission_classes = [IsAuthenticated,]

    def list (self, request):
        course_id = request.query_params.get('course_id', None)
        if course_id is None:
            return Response (
                    {"error": "expected 'course_id' parameter"},
                    status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(course=course_id)
        serializer = self.get_serializer(queryset, many=True)
        course_progress = models.CourseProgression.objects.filter(user=request.user).first()
        if course_progress is None:
            for module in serializer.data:
                module['completed'] = "false"
            return Response (serializer.data, status=status.HTTP_200_OK)

        current_module = self.get_queryset().filter(pk=course_progress.current_module).first()
        assert(current_module is not None)
        for module in serializer.data:
            if module.get('sort_index') < current_module.sort_index:
                module['completed'] = "false"
            elif module.get('sort_index') == current_module.sort_index:
                module['completed'] = "pending"
            else:
                module['completed'] = "true"

        return Response (serializer.data)

    def retrieve (self, request, pk):
        module: models.Module = self.get_object()
        course_progress = models.CourseProgression.objects.filter(user=request.user).first()
        if course_progress is None and int(pk) > 1:
            return Response ({"error": "Not allowed to access this module when the previous ones are not done"})

        if course_progress is not None:
            current_module = self.get_queryset().get(pk=course_progress.current_module)
            if module.sort_index > current_module.sort_index:
                return Response (
                        {"error":"Not allowed to access this module when the previous ones are not done"}
                        )

        serializer = self.get_serializer(module)
        return Response (serializer.data, status=status.HTTP_200_OK)

class ChapterViewSet (viewsets.ModelViewSet):
    queryset = models.Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer
    permission_classes = [IsAuthenticated,]

    def list (self, request):

        module_id = request.query_params.get('module_id', None)
        if module_id is None:
            return Response (
                    {"error":"expected 'module_id' parameter"},
                    status=status.HTTP_400_BAD_REQUEST)
        chapters = self.get_queryset().filter(module=module_id)
        serializer = self.get_serializer(chapters, many=True)

        current_progression = models.CourseProgression.objects.filter(user=request.user).first()
        if current_progression is None:
            for chapter in serializer.data:
                chapter["completed"] = False
            return Response (serializer.data)

        current_chapter = chapters.get(id=current_progression.current_chapter)
        if current_chapter is None:
            for chapter in serializer.data:
                chapter["completed"] = False
            return Response (serializer.data)

        for chapter in serializer.data:
            chapter_index = chapter.get('sort_index')
            current_index = chapter.get('sort_index')
            if chapter_index < current_index:
                chapter["completed"] = "true"
            elif chapter_index == current_index:
                chapter["completed"] = "pending"
            else:
                chapter["completed"] = "false"

        return Response (serializer.data)

    def retrieve (self, request, pk):
        chapter = self.get_object()
        course_progress = models.CourseProgression.objects.filter(user=request.user).first()
        if course_progress is None and int(pk) > 1:
            return Response (
                    {"error":"Not allowed to access this chapter when the previous ones are not done"}
                    )

        if course_progress is not None:
            current_chapter = self.get_queryset().get(pk=course_progress.current_chapter)
            if chapter.sort_index > current_chapter.sort_index:
                return Response (
                        {"error":"Not allowed to access this chapter when the previous ones are not done"}
                        )

        serializer = self.get_serializer(chapter)
        return Response (serializer.data, status=status.HTTP_200_OK)

class CompletedSignableViewSet (viewsets.ModelViewSet):
    queryset = models.CompletedSignable.objects.all()
    serializer_class = serializers.CompletedSignableSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list (self, request):
        chapter_id = request.query_params.get('chapter_id', None)
        if chapter_id is None:
            return Response ({"error":"Requires field 'chapter_id'!"})
        chapter: models.Chapter = models.Chapter.objects.get(pk=chapter_id)
        if not chapter.is_signable:
            return Response ({"error":"Chapter is not of signable type! Malformed request!"})

        completed_signables_for_chapter = self.get_queryset().filter(chapter=chapter_id)
        completed_words: list[str] = [signable.word for signable in completed_signables_for_chapter]
        chapter_content_filepath = os.path.join(settings.BASE_DIR, "content", chapter.content_filepath)

        response_json: dict = {}
        with open (chapter_content_filepath, newline='') as chapter_content:
            eng_swa = csv.reader(chapter_content, delimiter=',')
            words: list = []
            for row in eng_swa:
                words.append(
                        {
                            "english"   : row[0],
                            "swahili"   : row[1],
                            "completed" : True if row[0] in completed_words else False
                        }
                    )

        response_json["chapter_id"] = chapter_id
        response_json["chapter_content_filepath"] = chapter_content_filepath
        response_json["words"] = words

        return JsonResponse(response_json, status=status.HTTP_200_OK)

class CourseProgressionViewSet (viewsets.ModelViewSet):

    queryset = models.CourseProgression.objects.all()
    serializer_class = serializers.CourseProgressionSerializer
    permission_classes = [IsAuthenticated,]

    def create (self, request):
        instance = self.get_queryset().filter(user=request.user).first()
        is_updating = instance is not None

        serializer = self.get_serializer(instance, data=request.data, partial=is_updating)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        if is_updating:
            return Response (serializer.data, status=status.HTTP_200_OK)
        return Response (serializer.data, status=status.HTTP_201_CREATED)

class CompletedCourseViewSet (viewsets.ModelViewSet):
    queryset = models.CompletedCourse.objects.all()
    serializer_class = serializers.CompletedCourseSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
