from django.contrib import messages
from django.contrib.auth import logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from usuarios.forms import UserRegisterForm

from .models import Firm, User


def login(request):
    access_level = request.session.get('access_level', 0)
    if access_level != 0:
        return HttpResponseForbidden()

    context = {'access_level': access_level, }

    register_form_data = request.session.get('user_login', None)
    if register_form_data:
        context["email"] = register_form_data["email"]
        context["password"] = register_form_data["password"]

    return render(request, 'usuarios/pages/login.html', context)


def login_auth(request):
    POST = request.POST
    if not POST:
        raise Http404
    request.session['user_login'] = POST

    if POST['email'] and POST['password']:
        try:
            user = User.objects.get(
                email=POST['email'],
                password=POST['password'],
            )
        except User.DoesNotExist:
            messages.error(request, 'USUARIO OU SENHA INCORRETO')
            return redirect('users:login')

        del (request.session['user_login'])
        request.session['access_level'] = user.access_level
        request.session['firm'] = {
            'name': user.firm.name, 'id': user.firm_id}

        remember_me = False if POST.get('remember-me') else True
        if remember_me:
            request.session.set_expiry(0)
        return redirect('main:home')


def users(request):
    access_level = request.session.get('access_level', 0)
    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    if access_level == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect('users:login')

    context = {
        'access_level': access_level,
        'firm': firm['name'],
    }

    search = request.GET.get('pesquisa', False)
    users = User.objects.filter(
        firm_id=firm['id'], access_level=1)

    if search:
        context['back'] = True
        context['search'] = search
        users = User.objects.filter(
            firm_id=firm['id'],
            access_level=1,
            name__startswith=search
        )
    context['users'] = users

    return render(request, 'usuarios/pages/users.html', context)


def detailed_user(request, id):
    access_level = request.session.get('access_level', 0)
    if access_level == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect('users:login')

    firm = request.session.get('firm', {'nome': 'erro', 'id': 0})
    try:
        user = User.objects.get(
            firm_id=firm['id'],
            access_level=1,
            pk=id)
    except User.DoesNotExist:
        raise Http404

    return render(request, 'usuarios/pages/detailed_user.html', context={
        'user': user,
        'access_level': access_level,
        'complete': True,
    })


def user_registration(request):
    access_level = request.session.get('access_level', 0)
    if access_level != 2:
        return HttpResponseForbidden()

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    user_registration = request.session.get('user_registration', None)
    form = UserRegisterForm(user_registration)
    return render(request, 'usuarios/pages/user_registration.html', context={
        'access_level': access_level,
        'firm': firm['name'],
        'forms': form,
    })


def user_registration_auth(request):
    if not request.POST:
        raise Http404

    session_firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    POST = request.POST
    request.session['user_registration'] = POST
    form = UserRegisterForm(POST)
    if form.is_valid():
        del (request.session['user_registration'])
        firm = Firm.objects.get(pk=session_firm['id'])
        try:
            User.objects.create(
                email=request.POST['email'],
                password=request.POST['senha'],
                name=request.POST['nome'],
                access_level=1,
                firm=firm
            )
            messages.success(request, 'Usuário Cadastro com Sucesso')
        except IntegrityError:
            messages.error(
                request, 'Esse Usuário já foi cadastrado anteriomente')

    else:
        messages.error(request, 'Erro ao cadastrar o usuário')
    return redirect('users:user_registration')


def delete_user(request, id: int):
    if not request.POST:
        raise HttpResponseForbidden()

    firm = request.session.get('firm', {'nome': 'erro', 'id': 0})
    try:
        user = User.objects.get(
            firm_id=firm['id'],
            access_level=1,
            pk=id
        )
        user.delete()
        messages.success(request, 'Usuario apagado com sucesso')
    except User.DoesNotExist:
        messages.error(request, 'Não foi possível excluir esse Usuário')
        return redirect('users:users')

    return redirect('users:users')


def exit(request):
    logout(request)
    return redirect('main:home')
