from django.contrib import messages
from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import redirect, render

from main import forms, models


def home(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    return render(request, 'main/pages/home.html', context={
        'nv_acesso': nv_acesso,
    })


def login(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso != 0:
        raise Http404
    register_form_data = request.session.get('user_login', None)
    form = forms.UserLoginForm(register_form_data)
    return render(request, 'main/pages/login.html', context={
        'form': form,
        'nv_acesso': nv_acesso,
    })


def login_auth(request):
    POST = request.POST
    if not POST:
        raise Http404
    request.session['user_login'] = POST
    form = forms.UserLoginForm(POST)

    if form.is_valid():
        user_data = models.User.objects.filter(
            email=POST['email'],
            senha=POST['senha'],
        ).first()

        if user_data:
            del (request.session['user_login'])
            request.session['nv_acesso'] = user_data.nv_acesso
            request.session['empresa'] = {
                'nome': user_data.empresa.nome, 'id': user_data.empresa_id}

            lembre_me = False if POST.get('lembre_me') else True
            if lembre_me:
                request.session.set_expiry(0)
            return redirect('main:home')
    messages.error(request, 'USUARIO OU SENHA INCORRETO')
    return redirect('main:login')


def sobre(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    return render(request, 'main/pages/sobre.html', context={
        'nv_acesso': nv_acesso,
    })


def exit(request):
    logout(request)
    return redirect('main:home')
