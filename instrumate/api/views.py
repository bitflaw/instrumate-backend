from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import pymupdf
import sqlite3
import json
import os
import uuid
import json
import re
from nltk.tokenize import sent_tokenize
from rest_framework.response import Response
from rest_framework import status
from .utils.redis_client import redis_client

from translation_model.translate_to_ksl import eng_to_ksl_translator, ksl_to_eng_translator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text):
        # Remove invisible characters
        text = re.sub(r'[\u200b\u200c\u200d\u200e\u200f]', '', text)
        # Normalize spacing, remove bullet points
        text = text.replace('•', '').strip()
        text = re.sub(r'[ \t]+', ' ', text)
        return text

def split_sentences(text):
    cleaned = clean_text(text)
    return sent_tokenize(cleaned)


def split_words(sentence):
    # Split the sentence into words using regex to handle punctuation
    words = re.findall(r'\b\w+\b', sentence)
    return words


def reconstruct_sentences(sentences: list[str]) -> str:
    result = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # Capitalize first letter and add a period if missing
        sentence = sentence[0].upper() + sentence[1:]
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        result.append(sentence)
    return " ".join(result)


class HandleUpload(APIView):

    parser_classes = [MultiPartParser]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = ""
        self.image_paths = []
        self.chunks = {}
        self.page = {}
        self.translation = ""

    def file_chunker(self, file_path: str) -> None:
        document = pymupdf.open(file_path)
        self.chunks.clear()
        for page_no in range(0,document.page_count, 1):
            page = document.load_page(page_no)
            extracted_images = page.get_images()
            self.page["text"] = page.get_text()

            for index,img in enumerate(extracted_images):
                xref = img[0]
                pix = pymupdf.Pixmap(document, xref)
                img_path = f"/tmp/upload_dir/images/page{page_no}_img{index}.png"
                self.image_paths.append(f"/media/page{page_no}_img{index}.png")

                if pix.n > 5:
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

                pix.save(img_path)
                pix=None

            if self.image_paths:
                self.page["images"] = self.image_paths.copy()
            else:
                self.page["images"] = []
            self.image_paths.clear()

            self.page["symbols"] = []
            self.chunks[page_no] = self.page.copy()
            self.page.clear()

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error": "No uploaded file detected!"}, status=status.HTTP_400_BAD_REQUEST)

        self.file_name = uploaded_file.name

        tmp_img_dir = "/tmp/upload_dir/images"
        tmp_file_dir = "/tmp/upload_dir/files"
        if not os.path.exists(tmp_file_dir):
            os.makedirs(tmp_file_dir)
        tmp_file_path = os.path.join(tmp_file_dir, self.file_name)
        try:
            with open(tmp_file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # store chunks in redis
            self.file_chunker(tmp_file_path)
            for i in range(0, len(self.chunks),1):
                sentences: list[str] = split_sentences(self.chunks[i]["text"])
            task_id = str(uuid.uuid4())
            redis_client.setex(task_id, 300, json.dumps(sentences))  # Store for 5 minutes(300s)
            # Store context for the response
            context = {
                "task_id": task_id,
                "file_name": self.file_name,
                "chunks": self.chunks,
            }

            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Failed to write or chunk file")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServeFiles(APIView):

    def post(self, request, filename):
        image_filepath = os.path.join("/tmp/upload_dir/images/", filename)
        if not os.path.exists(image_filepath):
            return Response({"error": "Image requested not found"}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(image_filepath, 'rb'), content_type='image/png')


class Eng_To_KSL(APIView):
    def post(self, request):
        # Step 1: Get task_id from request
        task_id = request.data.get("task_id")
        if not task_id:
            return Response({"error": "task_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

        redis_key = task_id
        # load cached sentences from Redis
        cached_sentences = redis_client.get(redis_key)
        if not cached_sentences:
            return Response(
                    {"error": "No cached data found for the provided task_id"},
                    status=status.HTTP_404_NOT_FOUND
                    )
        # Step 2: Parse the cached sentences
        dict_cached_sentences = json.loads(str(cached_sentences))
        # Step 3: Translate each sentence
        translated_sentences = []
        for sentence in dict_cached_sentences:
            sentence_key = f"{task_id}:{sentence}"
            # Check if translation is cached. If cached, use it, otherwise translate and cache it
            cached_translation = redis_client.get(sentence_key)
            if cached_translation:
                translation = cached_translation
            else:
                translation = eng_to_ksl_translator(sentence)
                redis_client.set(sentence_key, translation, ex=300) # Cache for 5 minutes

            translated_sentences.append(translation)
        # Step 4: Reconstruct the full translation
        full_translation = reconstruct_sentences(translated_sentences)
        translated_sentences = split_sentences(full_translation)
        words = []
        for sentence in translated_sentences:
            sentence_words = split_words(sentence)
            words.extend(sentence_words)
        # Step 5: Cache the full translation and words to be sent to BVH
        full_translation_key = f"{task_id}:full_translation"
        redis_client.setex(full_translation_key, 300, json.dumps(words))  # Store for 5 minutes
        # Step 4: Return the full translation and original sentences
        context = {
            "task_id": full_translation_key,
            "translated_sentences": translated_sentences,
            "original_sentences": dict_cached_sentences,
            "words": words
        }
        return Response(context, status=status.HTTP_200_OK)


class KSL_To_Eng(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        translation = ksl_to_eng_translator(text)
        return Response ({"translation": translation}, status=status.HTTP_200_OK)

class Animations (APIView):

    # permission_classes = [IsAuthenticated,]

    def get (self, request):
        text = request.data.get ("text")
        if text is None:
            return Response ({"message": "Nothing to get animation data for!"}, 400)
        words: list[str] = text.split(' ')
        animation_data = []
        dataset_filepath = os.path.join(settings.BASE_DIR, "dataset.sqlite3.db")
        cxn = sqlite3.connect(dataset_filepath)
        cursor = cxn.cursor()
        placeholders = ', '.join(['?'] * len(words))
        query = f"SELECT ani_data FROM records WHERE name IN ({placeholders})"
        cursor.execute(query, words)
        data =  cursor.fetchall()
        for d in data:
            blob = json.loads(str(d[0].decode('utf-8')))
            animation_data += blob

        cursor.close()
        cxn.close()
        return Response ({"data": animation_data}, 200)
