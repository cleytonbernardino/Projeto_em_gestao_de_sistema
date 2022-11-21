from os import environ
from urllib.request import urlretrieve

from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from geopandas.tools import reverse_geocode
from geopy.exc import GeocoderTimedOut
from shapely.geometry import Point

from .forms import PlacaForm, VeiculoForm
from .models import Veiculo, VeiculoHistorico

"""
    EU VOU ARRUMAR TODO ESSE CODIGO, UMA HORA.
"""


def veiculos(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso == 0:
        messages.error(request, 'Você deve está logado para poder fazer isso')
        return redirect('main:login')

    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    pesquisa = request.GET.get('pesquisa', None)
    veiculos = Veiculo.objects.filter(empresa_id=empresa['id'])
    if pesquisa:
        veiculos = Veiculo.objects.get(
            empresa_id=empresa['id'], placa=pesquisa)

    return render(request, 'veiculos/pages/veiculos.html', context={
        'empresa': empresa['nome'],
        'nv_acesso': nv_acesso,
        'veiculos': veiculos,
    })


def veiculo_completo(request, id):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso == 0:
        messages.error(request, 'Você deve está logado para poder fazer isso')
        return redirect('main:login')

    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    veiculo = Veiculo.objects.get(empresa_id=empresa['id'], pk=id)
    return render(request, 'veiculos/pages/veiculo_completo.html', context={
        'empresa': empresa['nome'],
        'nv_acesso': nv_acesso,
        'veiculo': veiculo,
        'completo': True,
    })


def veiculo_cadastro(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso != 2:
        return HttpResponseForbidden()

    veiculo_form_data = request.POST.get('veiculo_form_data', None)
    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    return render(request, 'veiculos/pages/cadastro_veiculos.html', context={
        'nv_acesso': nv_acesso,
        'empresa': empresa['nome'],
        'forms': VeiculoForm(veiculo_form_data),
    })


def veiculo_cadastro_auth(request):
    POST = request.POST
    if not POST:
        raise Http404

    form = VeiculoForm(POST, request.FILES)
    request.session['veiculo_form_data'] = POST
    if form.is_valid():
        del (request.session['veiculo_form_data'])
        Veiculo.objects.create(
            empresa_id=request.session['empresa']['id'],
            proprietario=POST['proprietario'],
            foto_carro=request.FILES['foto_veiculo'],
            modelo=POST['modelo'],
            pais=POST['pais'],
            placa=POST['placa'],
            num_chassi=POST['num_chassi'],
        )
        messages.success(request, 'Veículo cadastrado com sucesso')
        return redirect('veiculos:veiculo_cadastro')
    messages.info(request, 'Não foi possivel cadastrar esse veículo')
    return redirect('veiculos:veiculo_cadastro')


def pegar_cordenadas(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    return render(request, 'veiculos/pages/simular_carro.html', context={
        'nv_acesso': nv_acesso,
    })


def salvar_cordenadas(request):
    POST = request.POST
    if not POST:
        raise Http404
    veiculo = Veiculo.objects.get(placa=POST['placa'])
    VeiculoHistorico.objects.create(
        veiculo=veiculo,
        latitude=POST['latitude'],
        longitude=POST['longitude']
    )
    return redirect('veiculos:pegar_cordenadas')


def historico(request, placa: str):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso == 0:
        raise HttpResponseForbidden()

    empresa = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    usadas = []
    historico = []
    try:
        veiculo = Veiculo.objects.get(empresa_id=empresa['id'], placa=placa)
        cordenadas = VeiculoHistorico.objects.filter(
            veiculo=veiculo).order_by('-pk')

        for cordenada in cordenadas:
            tentativa = 0
            latitude = cordenada.latitude
            longitude = cordenada.longitude
            if latitude and longitude in usadas:
                continue
            point = Point(float(latitude),
                          float(longitude))
            try:
                endereco = reverse_geocode(point).address[0]
            except GeocoderTimedOut:
                if tentativa == 3:
                    historico = ['Não foi possivel localizar o historico, tente novamente mais tarde']  # noqa: E501
                    break
                tentativa += 1
            usadas.append(latitude)
            usadas.append(longitude)
            historico.append(endereco)
    except Veiculo.DoesNotExist:
        historico.append('Este Veículo não existe')

    return render(request, 'veiculos/pages/historico.html', context={
        'nv_acesso': nv_acesso,
        'historico': historico,
    })


def gerar_mapa(latitude: float, longitude: float):
    url_confg = {
        'api_key': environ.get('api_key'),
        'latitude': latitude,
        'longitude': longitude,
    }
    URL = (
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"center={url_confg['latitude']},{url_confg['longitude']}"
        f"&markers={url_confg['latitude']},{url_confg['longitude']}"
        f"&zoom=17&size=1000x480&scale=2&key={url_confg['api_key']}"
    )
    # urlretrieve(URL, 'media/main/mapa/mapa.jpg')


def pesquisa_avancada(request):
    nv_acesso = request.session.get('nv_acesso', 0)
    if nv_acesso == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect("main:login")

    pesquisa = None
    end = 'Não Disponivel'
    if request.GET:
        # request.GET['placa']
        try:
            pesquisa = Veiculo.objects.get(
                empresa_id=request.session['empresa']['id'],
                placa='UNO2L75',
            )
            historico = VeiculoHistorico.objects.filter(
                veiculo=pesquisa
            ).order_by('-pk')[0]
            end = reverse_geocode(
                Point(float(historico.latitude), float(historico.longitude))).address[0]
            gerar_mapa(float(historico.latitude), float(historico.longitude))
        except Veiculo.DoesNotExist:
            pass

    return render(request, 'veiculos/pages/pesquisa_avancada.html', context={
        'forms': PlacaForm(),
        'resultado': pesquisa,
        'localizacao': end.split(',')[0],
        'nv_acesso': nv_acesso,
    })
