from django.db import models

from usuarios.models import Firm


class Vehicle(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    owner = models.CharField(max_length=50)
    photo_car = models.ImageField(
        'Imagem do Veículo', upload_to='main/carros/%Y/%m/%d/')
    model = models.CharField("Modelo do Veículo", max_length=50)
    color = models.CharField('Cor do veículo', max_length=10)
    country = models.CharField("País", max_length=50, default="Brasil")
    license_plate = models.CharField("Placa", max_length=7, unique=True)
    num_frame = models.CharField(
        "Número do Chassi", max_length=20, unique=True)

    def __str__(self):
        return f'{self.firm} ({self.license_plate})'


class VehicleHistoric(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    time = models.DateTimeField('Data e Hora', auto_now_add=True)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.license_plate
