import time

from django.http import JsonResponse
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
from .tasks import send_invoice_email, send_notify, test_retry
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
import json
import logging


logger = logging.getLogger(__name__)
logger.info("📢 Log INFO từ logger hoạt động!")
logger.debug("🐞 Log DEBUG từ logger hoạt động!")


def hello_view(request):
    return JsonResponse({"message": "Hello Django!"})


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def list(self, request, *args, **kwargs):
        cache_key = "note_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info("📦 Trả từ Redis cache (ViewSet)")
            return Response(json.loads(cached_data))

        logger.info("🗃️ Lấy từ DB rồi cache (ViewSet)")
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, json.dumps(response.data), timeout=60)
        return response


@api_view(['GET'])
def place_order(request):
    # pretend this saves an order
    order_id = 1235  # this would come from your model

    # run the task in the background
    send_invoice_email.delay(order_id)
    send_notify.delay(order_id)
    # test_retry.delay(order_id)

    time.sleep(1)

    return JsonResponse({"message": "Request done!"})


class CachedNoteList(APIView):
    def get(self, request):
        cache_key = "note_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info("📦 Trả từ Redis cache")
            return Response(json.loads(cached_data))

        # Nếu chưa có cache
        logger.info("🗃️ Lấy từ DB rồi cache")
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        data = serializer.data

        cache.set(cache_key, json.dumps(data), timeout=15)  # cache 60s
        return Response(data)
