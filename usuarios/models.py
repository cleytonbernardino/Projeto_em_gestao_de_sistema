from django.db import models


class Firm(models.Model):
    name = models.CharField("Nome da Empresa", max_length=50)
    cnpj = models.CharField("CNPJ", max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    name = models.CharField("Nome Completo", max_length=100)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField("Senha", max_length=255)
    access_level = models.IntegerField("Nível de Aceso", choices=[
        (1, 'Nível 1'),
        (2, 'Nível 2'),
    ], default=1)

    def __str__(self):
        return f"{self.name} ({self.firm})"
