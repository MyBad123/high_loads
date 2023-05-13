from django.contrib import admin
from django.urls import path

from app.views.auth_views import auth, Auth
from app.views.source_views import SourceView
from app.views.results_view import ListResultView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', auth),
    path('auth-class/', Auth.as_view()),
    path('form/', SourceView.as_view()),
    path('list/', ListResultView.as_view()),
]
