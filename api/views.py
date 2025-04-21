from django.http import JsonResponse
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer


def hello_view(request):
    return JsonResponse({"message": "Hello Django!"})


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
