from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from main.models import Empresa, User
from usuarios.forms import UserRegisterForm


def usuarios(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    if nv_acesso == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect('main:login')

    voltar = False
    pesquisa = request.GET.get('pesquisa', False)
    usuarios = User.objects.filter(
        empresa_id=empresa['id'], nv_acesso=1)
    if pesquisa:
        voltar = True
        usuarios = User.objects.filter(
            empresa_id=empresa['id'], nv_acesso=1, nome__startswith=pesquisa)
    return render(request, 'usuarios/pages/usuarios.html', context={
        'usuarios': usuarios,
        'nv_acesso': nv_acesso,
        'empresa': empresa['nome'],
        'voltar': voltar,
    })


def usuario_detalhado(request, id):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect('main:login')
    usuario = User.objects.get(pk=id)
    return render(request, 'usuarios/pages/usuario_completo.html', context={
        'usuario': usuario,
        'nv_acesso': nv_acesso,
        'completo': True,
    })


def usuario_cadastro(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso != 2:
        return HttpResponseForbidden()

    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    usuarios_cadastro = request.session.get('usuarios_cadastro', None)
    form = UserRegisterForm(usuarios_cadastro)
    return render(request, 'usuarios/pages/cadastro_usuarios.html', context={
        'nv_acesso': nv_acesso,
        'empresa': empresa['nome'],
        'forms': form,
    })


def usuario_cadastro_auth(request):
    if not request.POST:
        raise Http404

    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    POST = request.POST
    request.session['usuarios_cadastro'] = POST
    form = UserRegisterForm(POST)
    if form.is_valid():
        empresa_db = Empresa.objects.get(pk=empresa['id'])
        User.objects.create(
            email=request.POST['email'],
            senha=request.POST['senha'],
            nome=request.POST['nome'],
            nv_acesso=1,
            empresa=empresa_db
        )
        messages.success(request, 'Usuario Cadastro com Sucesso')
        del (request.session['usuarios_cadastro'])
    else:
        messages.error(request, 'Erro ao cadastrar o usuario')
    return redirect('usuarios:usuario_cadastro')


def delete_user(request):
    if not request.POST:
        raise HttpResponseForbidden()

    email = request.POST.get('email', None)
    business = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    if email is None:
        return redirect('usuarios:usuarios')  # Colocar uma message falando que não pode ser excluido # noqa: E501

    User.objects.delete(
        empresa_id=business['id'],
        email=email
    )
    return redirect('usuarios:usuarios')
