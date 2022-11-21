from django.db import models


class Empresa(models.Model):
    nome = models.CharField("Nome da Empresa", max_length=50)
    cnpj = models.CharField("CNPJ", max_length=50, unique=True)

    def __str__(self):
        return self.nome


class User(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField("Nome Completo", max_length=100)
    email = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=255)
    nv_acesso = models.IntegerField("Nível de Aceso", choices=[
        (1, 'Nivel1'),
        (2, 'Nivel2'),
    ], default=1)

    def __str__(self):
        # SIM ISSO É UM ERRO DE SEGURANÇA EU VOU TIRAR DPS
        # É SO PARA EU PODER PROGRAMAR MAIS FACÍMENTE
        return self.email
