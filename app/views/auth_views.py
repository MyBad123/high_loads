from math import erf
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views import View


def auth(request):
    return render(request, 'reg.html')


class Authentication:
    
    @staticmethod
    def is_true(login: str, password: str):
        user = authenticate()


class Auth(View):
    def get(self, request, *args, **kwargs):
        """get form for auth"""

        error = request.GET.get('error', None)
        if error == 'error':
            template_error = True
        else:
            template_error = False

        return render(request, 'reg.html', context={
            'template_error': template_error
        })

    def post(self, request, *args, **kwargs):
        print(request.POST)
        
        return redirect('/auth-class/')
