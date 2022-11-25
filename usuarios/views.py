from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from main.models import Empresa, User
from usuarios.forms import UserRegisterForm


def users(request):
    access_level = request.session.get('access_level', 0)
    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    if access_level == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect('main:login')

    context = {
        'access_level': access_level,
        'firm': firm['name'],
    }

    search = request.GET.get('pesquisa', False)
    users = User.objects.filter(
        empresa_id=firm['id'], nv_acesso=1)

    if search:
        context['back'] = True
        context['search'] = search
        users = User.objects.filter(
            empresa_id=firm['id'],
            nv_acesso=1,
            nome__startswith=search
        )
    context['users'] = users

    return render(request, 'usuarios/pages/users.html', context)


def detailed_user(request, id):
    access_level = request.session.get('access_level', 0)
    if access_level == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect('main:login')

    firm = request.session.get('firm', {'nome': 'erro', 'id': 0})
    try:
        user = User.objects.get(
            empresa_id=firm['id'],
            nv_acesso=1,
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
        firm = Empresa.objects.get(pk=session_firm['id'])
        try:
            User.objects.create(
                email=request.POST['email'],
                senha=request.POST['senha'],
                nome=request.POST['nome'],
                nv_acesso=1,
                empresa=firm
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
            empresa_id=firm['id'],
            nv_acesso=1,
            pk=id
        )
        user.delete()
        messages.success(request, 'Usuario apagado com sucesso')
    except User.DoesNotExist:
        messages.error(request, 'Não foi possível excluir esse Usuário')
        return redirect('users:users')

    return redirect('users:users')
