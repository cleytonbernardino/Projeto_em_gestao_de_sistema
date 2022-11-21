from os import environ

# from urllib.request import urlretrieve
# from geopandas.tools import reverse_geocode
from geopy.exc import GeocoderTimedOut

from .models import Veiculo, VeiculoHistorico


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


def buscar_veiculo(empresa_id: int, placa: str = ''):
    pesquisa = None
    try:
        pesquisa = Veiculo.objects.get(
            empresa_id=empresa_id,
            placa='UNO2L75',
        )
        historico = VeiculoHistorico.objects.filter(
            veiculo=pesquisa
        ).order_by('-pk')[0]
        tentativa = 0
        while tentativa < 3:
            try:
                # endereco = reverse_geocode(
                # Point(float(historico.latitude), float(historico.longitude))).address[0] #noqa: E501
                endereco = 'Nada por enquanto'
                break
            except GeocoderTimedOut:
                tentativa += 1
    except Veiculo.DoesNotExist:
        pesquisa = {
            'modelo': 'Desconhecido',
            'proprietario': 'Desconhecido(a)',
            'pais': 'Desconhecido',
            'placa': placa if placa != '' else 'Desconhecido',
            'num_chassi': 'Desconhecido',
            'localizacao': 'Desconhecida'
        }
    return pesquisa
