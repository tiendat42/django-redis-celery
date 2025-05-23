from django.urls import path, include
from .views import hello_view, NoteViewSet, place_order
from rest_framework.routers import DefaultRouter
from .views import CachedNoteList


router = DefaultRouter()
router.register(r'notes-viewset', NoteViewSet)


urlpatterns = [
    path('hello/', hello_view),
    path('', include(router.urls)),
    path('place_order/', place_order),
    path('notes-apiview/', CachedNoteList.as_view()),
]
