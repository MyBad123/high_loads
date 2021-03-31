from rest_framework import routers
from .views import SnippetViewSet

router = routers.DefaultRouter()
router.register('snippets', SnippetViewSet)
