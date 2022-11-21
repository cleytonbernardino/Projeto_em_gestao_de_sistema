from django.db import models
from main.models import Empresa


class Veiculo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    proprietario = models.CharField(max_length=50)
    foto_carro = models.ImageField('Imagem do Veículo',
                                   upload_to='main/carros/%Y/%m/%d/'
                                   )
    modelo = models.CharField("Modelo do Veículo", max_length=50)
    cor = models.CharField('Cor do veículo', max_length=10, null=True)
    pais = models.CharField(max_length=50)
    placa = models.CharField(max_length=7, unique=True)
    num_chassi = models.CharField(
        "Número do Chassi", max_length=17, unique=True)

    def __str__(self):
        return self.placa


class VeiculoHistorico(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    horario = models.DateTimeField('Data e Hora', auto_now_add=True)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.veiculo.placa
