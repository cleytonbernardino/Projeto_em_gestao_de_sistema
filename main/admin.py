from django.contrib import admin
from veiculos.models import Veiculo, VeiculoHistorico

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    pass


@admin.register(VeiculoHistorico)
class VeiculoHistoricoAdmin(admin.ModelAdmin):
    pass
