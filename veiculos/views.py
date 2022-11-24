# from urllib.request import urlretrieve

from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from . import views_utilities as ult
from .forms import VeiculoForm
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
        veiculos = Veiculo.objects.filter(
            empresa_id=empresa['id'],
            placa__startswith=pesquisa.upper())

    return render(request, 'veiculos/pages/vehicles.html', context={
        'empresa': empresa['nome'],
        'nv_acesso': nv_acesso,
        'veiculos': veiculos,
    })


def complete_vehicle(request, license_plate: str):
    access_level = request.session.get('nv_acesso', 0)
    if access_level == 0:
        messages.error(request, 'Você deve está logado para poder fazer isso')
        return redirect('main:login')

    business = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    vehicle = ult.get_vehicle(business['id'], license_plate)
    if type(vehicle) != Veiculo:
        raise Http404

    return render(request, 'veiculos/pages/complete_vehicle.html', context={
        'empresa': business['nome'],
        'nv_acesso': access_level,
        'veiculo': vehicle,
        'completo': True,
    })


def vehicle_registration(request):
    access_level = request.session.get('nv_acesso', 0)
    if access_level != 2:
        return HttpResponseForbidden()

    veiculo_form_data = request.POST.get('veiculo_form_data', None)
    business = request.session.get('business', {'nome': 'erro', 'id': 0})
    return render(request, 'veiculos/pages/cadastro_veiculos.html', context={
        'nv_acesso': access_level,
        'empresa': business['nome'],
        'forms': VeiculoForm(veiculo_form_data),
    })


def registration_vehicle_auth(request):
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


def edit_vehicle(request, license_plate: str):
    access_level = request.session.get('nv_acesso', 0)
    if access_level != 2:
        raise HttpResponseForbidden()

    business = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    vehicle = ult.get_vehicle(business['id'], license_plate)

    if type(vehicle) != Veiculo:
        return Http404

    return render(request, 'veiculos/pages/edit_vehicle.html', {
        'nv_acesso': access_level,
        'business': business['nome'],
        'vehicle': vehicle
    })


def edit_vehicle_auth(request, license_plate: str):
    POST = request.POST
    if not POST:
        raise HttpResponseForbidden()

    business = request.session.get('business', {'nome': 'erro', 'id': 0})
    vehicle = ult.get_vehicle(business['id'], license_plate)
    if vehicle is None:
        return Http404

    vehicle.proprietario = POST["proprietario"]
    vehicle.modelo = POST["modelo"]
    vehicle.cor = POST["cor"]
    vehicle.placa = POST["placa"]
    if request.FILES:
        vehicle.foto_carro = request.FILES["foto"]


def delete_vehicle(request, license_plate: str):
    if not request.POST:
        raise Http404

    business = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    try:
        vehicle = ult.get_vehicle(business['id'], license_plate)
        vehicle.delete()
        messages.success(request, 'Veículo apagado com sucesso')
    except Veiculo.DoesNotExist:
        messages.error(request, 'Não foi possível apagar esse veículo')

    return redirect('veiculos:veiculos')


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


def historic(request, license_plate: str):
    access_level = request.session.get('nv_acesso', 0)
    if access_level == 0:
        raise HttpResponseForbidden()

    business = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    used = []
    streets = {}

    vehicle = ult.get_vehicle(business['id'], license_plate)
    if type(vehicle) != Veiculo:
        raise Http404

    historic = ult.get_historic(vehicle)
    if historic is None:
        streets['00/00/0000 00:00'] = 'Esse Veículo não possui Histórico ainda'
    else:
        for i in historic:
            lati = float(i.latitude)
            long = float(i.longitude)
            if long not in used:
                time = i.horario
                formated_time = f'{time.day}/{time.month}/{time.year}  {time.hour}:{time.minute}'  # noqa: E501
                streets[f'{formated_time}'] = ult.get_address(lati, long)
                used.append(long)

    return render(request, 'veiculos/pages/historic.html', context={
        'nv_acesso': access_level,
        'streets': streets,
        'license_plate': vehicle.placa,
    })


def search(request):
    access_level = request.session.get('nv_acesso', 0)
    if access_level == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect("main:login")

    historic = None
    street = 'Desconhecido'
    business = request.session.get('empresa', {'nome': 'erro', 'id': 0})
    placa = request.GET.get('placa', '')
    vehicle = ult.get_vehicle(business['id'], placa)

    if type(vehicle) == Veiculo:
        try:
            historic = ult.get_historic(vehicle)
            lati = float(historic[0].latitude)
            long = float(historic[0].longitude)
            ult.gerar_mapa(lati, long)
            street = ult.get_address(lati, long)
        except IndexError:
            street = 'Esse veículo não possuí historico de localização'
            # ADICIONAR DEPOIS UM SISTEMA DE TROCA DE MAPA

    return render(request, 'veiculos/pages/search.html', context={
        'vehicle': vehicle,
        'street': street,
        'empresa': business['nome'],
        'nv_acesso': access_level,
    })
