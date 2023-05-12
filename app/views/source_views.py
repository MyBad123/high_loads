from django.views import View
from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from app.forms import AllForms


class SourceView(View):
    """requests for get and set form with source"""

    q: str
    form: dict

    def invalid_form(self, request):
        # control request params
        self.q = request.GET.get('param', None)
        if self.q is None:
            return True

        # control paraf from request
        self.form = AllForms.get(self.q, None)
        if self.form is None:
            return True

        return False

    def get(self, request, *args, **kwargs):
        # control params from request
        if self.invalid_form(request):
            return redirect('/')
        
        form_obj = self.form.get('form')()
        
        return render(request, 'form.html', context={
            'fields': form_obj.get_fields(),
            'url': self.q
        })
    
    def post(self, request, *args, **kwargs):
        """set new resource to db"""

        if self.invalid_form(request):
            return redirect('/')

        form_obj = self.form.get('form')({
            'surname': request.POST.get('surname', None),
            'initials': request.POST.get('initials', None),
            'title': request.POST.get('title', None),
            'place': request.POST.get('place', None),
            'publishing': request.POST.get('publishing', None),
            'year': request.POST.get('year', None),
            'pages': request.POST.get('pages', None)
        })

        if form_obj.is_valid():
            form_obj.save(self.form.get('model'))
            return redirect('/form/?param=book')
        else:
            return render(request, 'form.html', context={
                'fields': form_obj.get_fields_with_errors(),
                'url': self.q
            })
