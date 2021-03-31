from .models import Snippet
from .serializer import SnippetSerializer
from rest_framework import viewsets

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer






