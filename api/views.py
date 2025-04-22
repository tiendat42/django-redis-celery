import time

from django.http import JsonResponse
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
from .tasks import send_invoice_email, send_notify
from rest_framework.decorators import api_view


def hello_view(request):
    return JsonResponse({"message": "Hello Django!"})


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

@api_view(['GET'])
def place_order(request):
    # pretend this saves an order
    order_id = 1235  # this would come from your model

    # run the task in the background
    send_invoice_email.delay(order_id)
    send_notify.delay(order_id)

    time.sleep(2)

    return JsonResponse({"message": "Request done!"})
