from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from . import views_utilities as ult
from .forms import VeiculoForm
from .models import Vehicle, VehicleHistoric


def vehicles(request):
    access_level = request.session.get('access_level', 0)
    if access_level != 2:
        return HttpResponseForbidden()

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    search = request.GET.get('pesquisa', None)
    vehicles = Vehicle.objects.filter(firm_id=firm['id'])

    context = {
        'firm': firm['name'],
        'access_level': access_level,
        'vehicles': vehicles,
    }

    if search:
        context['vehicles'] = Vehicle.objects.filter(
            firm_id=firm['id'],
            placa__startswith=search.upper())
        context['back'] = True
        context['search'] = search

    return render(request, 'veiculos/pages/vehicles.html', context)


def complete_vehicle(request, license_plate: str):
    access_level = request.session.get('access_level', 0)
    if access_level != 2:
        return HttpResponseForbidden()

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    vehicle = ult.get_vehicle(firm['id'], license_plate)
    if type(vehicle) != Vehicle:
        raise Http404

    return render(request, 'veiculos/pages/complete_vehicle.html', context={
        'firm': firm['name'],
        'access_level': access_level,
        'vehicle': vehicle,
        'complete': True,
    })


def vehicle_registration(request):
    access_level = request.session.get('access_level', 0)
    if access_level != 2:
        return HttpResponseForbidden()

    veiculo_form_data = request.POST.get('veiculo_form_data', None)
    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    return render(request, 'veiculos/pages/vehicle_registration.html', context={  # noqa: E501
        'access_level': access_level,
        'firm': firm['name'],
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
        try:
            Vehicle.objects.create(
                firm_id=request.session['firm']['id'],
                owner=POST['proprietario'],
                photo_car=request.FILES['foto_veiculo'],
                model=POST['modelo'],
                country=POST['pais'],
                color=POST['cor'],
                license_plate=POST['placa'].upper(),
                num_frame=POST['num_chassi'],
            )
            messages.success(request, 'Veículo cadastrado com sucesso')
            return redirect('vehicles:vehicle_registration')
        except IntegrityError:
            messages.error(
                request, 'Esse Veícula já foi cadastro em nosso sistema, anteriomente')  # noqa: E501
    else:
        messages.info(
            request, 'Não foi possivel cadastrar esse veículo, por um motivo desconhecido')  # noqa: E501
    return redirect('vehicles:vehicle_registration')


def edit_vehicle(request, license_plate: str):
    access_level = request.session.get('access_level', 0)
    if access_level != 2:
        raise HttpResponseForbidden()

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    vehicle = ult.get_vehicle(firm['id'], license_plate)

    if type(vehicle) != Vehicle:
        return Http404

    return render(request, 'veiculos/pages/edit_vehicle.html', {
        'access_level': access_level,
        'firm': firm['name'],
        'vehicle': vehicle
    })


def edit_vehicle_auth(request, license_plate: str):
    POST = request.POST
    if not POST:
        raise Http404

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    vehicle = ult.get_vehicle(firm['id'], license_plate)
    if vehicle is None:
        return Http404

    vehicle.owner = POST["owner"]
    vehicle.model = POST["model"]
    vehicle.color = POST["color"]
    vehicle.license_plate = POST["license_plate"]
    if request.FILES:
        vehicle.photo_car = request.FILES["photo"]
    vehicle.save()

    return redirect(reverse("vehicles:complete_vehicle",
                            kwargs={"license_plate": vehicle.license_plate}))


def delete_vehicle(request, license_plate: str):
    if not request.POST:
        raise Http404

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    try:
        vehicle = ult.get_vehicle(firm['id'], license_plate)
        vehicle.delete()
        messages.success(request, 'Veículo apagado com sucesso')
    except Vehicle.DoesNotExist:
        messages.error(request, 'Não foi possível apagar esse veículo')

    return redirect('vehicles:vehicles')


def get_coordinates(request):
    access_level = request.session.get('access_level', 0)
    return render(request, 'veiculos/pages/simulate_vehicle.html', context={
        'access_level': access_level,
    })


def save_coordinates(request):
    POST = request.POST
    if not POST:
        raise Http404
    vehicle = Vehicle.objects.get(placa=POST['placa'])
    VehicleHistoric.objects.create(
        veiculo=vehicle,
        latitude=POST['latitude'],
        longitude=POST['longitude']
    )
    return redirect('vehicles:get_coordinates')


def historic(request, license_plate: str):
    access_level = request.session.get('access_level', 0)
    if access_level != 2:
        raise HttpResponseForbidden()

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    used = []
    streets = {}

    vehicle = ult.get_vehicle(firm['id'], license_plate)
    if type(vehicle) != Vehicle:
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
        'access_level': access_level,
        'streets': streets,
        'license_plate': vehicle.license_plate,
    })


def search(request):
    access_level = request.session.get('access_level', 0)
    if access_level == 0:
        messages.error(
            request, 'Você deve Estar logado para poder fazer isso.')
        return redirect("users:login")

    firm = request.session.get('firm', {'name': 'erro', 'id': 0})
    placa = request.GET.get('placa', '')
    vehicle = ult.get_vehicle(firm['id'], placa)

    context = {
        'access_level': access_level,
        'firm': firm['name'],
        'street': 'Esse veículo não possuí historico de localização',
        'vehicle': vehicle
    }

    if type(vehicle) == Vehicle:
        historic = ult.get_historic(vehicle)
        if historic is not None:
            lati = float(historic[0].latitude)
            long = float(historic[0].longitude)
            ult.generate_map(lati, long)
            context['street'] = ult.get_address(lati, long)
        else:
            pass  # Make a map swap for nothing

    return render(request, 'veiculos/pages/search.html', context)
