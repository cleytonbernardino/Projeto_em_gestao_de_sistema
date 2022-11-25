from os import environ

# from urllib.request import urlretrieve
from geopandas.tools import reverse_geocode
from geopy.exc import GeocoderTimedOut
from shapely.geometry import Point

from .models import Veiculo, VeiculoHistorico


def generate_map(latitude: float, longitude: float):
    url_confg = {
        'api_key': environ.get('api_key'),
        'latitude': latitude,
        'longitude': longitude,
    }
    URL = (  # noqa: F841
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"center={url_confg['latitude']},{url_confg['longitude']}"
        f"&markers={url_confg['latitude']},{url_confg['longitude']}"
        f"&zoom=17&size=1000x480&scale=2&key={url_confg['api_key']}"
    )
    # urlretrieve(URL, 'media/main/mapa/mapa.jpg')


def get_vehicle(firm_id: int, license_plate: str = ''):
    try:
        return Veiculo.objects.get(
            empresa_id=firm_id,
            placa=license_plate
        )
    except Veiculo.DoesNotExist:
        return {
            'foto_carro': {
                'url': '/media/main/mapa/logo.png',
            },
            'modelo': 'Desconhecido',
            'proprietario': 'Desconhecido(a)',
            'pais': 'Desconhecido',
            'cor': 'Desconhecida',
            'placa': license_plate if license_plate != '' else 'Desconhecida',
        }


def get_historic(vehicle: Veiculo):
    if type(vehicle) != Veiculo:
        raise ValueError()

    historic = VeiculoHistorico.objects.filter(
        veiculo=vehicle
    ).order_by('-pk')
    return historic if historic else None


def get_address(latitude: float, longitude: float):
    if type(latitude) != float or type(longitude) != float:
        raise ValueError()

    try:
        address = reverse_geocode(Point(latitude, longitude))
        return ''.join(address.address[0].split(',')[0])
    except GeocoderTimedOut:
        return 'Tempo Expirado'
    except AttributeError:
        return 'Não foi possível encontrar essa cordernada'
