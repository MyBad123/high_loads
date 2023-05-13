from django.views import View
from django.shortcuts import redirect, render
from django.views.generic.list import ListView

from app.models import Book


class ListResultView(ListView):
    model = Book
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
