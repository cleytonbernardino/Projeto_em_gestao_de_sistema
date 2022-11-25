from django.contrib import messages
from django.contrib.auth import logout
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from .models import User


def home(request):
    access_level = request.session.get('access_level', 0)
    return render(request, 'main/pages/home.html', context={
        'access_level': access_level,
    })


def login(request):
    access_level = request.session.get('access_level', 0)
    if access_level != 0:
        return HttpResponseForbidden()

    context = {'access_level': access_level, }

    register_form_data = request.session.get('user_login', None)
    if register_form_data:
        context["email"] = register_form_data["email"]
        context["password"] = register_form_data["password"]

    return render(request, 'main/pages/login.html', context)


def login_auth(request):
    POST = request.POST
    if not POST:
        raise Http404
    request.session['user_login'] = POST

    if POST['email'] and POST['password']:
        try:
            user = User.objects.get(
                email=POST['email'],
                senha=POST['password'],
            )
        except User.DoesNotExist:
            messages.error(request, 'USUARIO OU SENHA INCORRETO')
            return redirect('main:login')

        del (request.session['user_login'])
        request.session['access_level'] = user.nv_acesso
        request.session['firm'] = {
            'name': user.empresa.nome, 'id': user.empresa_id}

        remember_me = False if POST.get('remember-me') else True
        if remember_me:
            request.session.set_expiry(0)
        return redirect('main:home')


def about(request):
    access_level = request.session.get('access_level', 0)
    return render(request, 'main/pages/about.html', context={
        'access_level': access_level,
    })


def exit(request):
    logout(request)
    return redirect('main:home')
