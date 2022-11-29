from django.contrib import admin

from usuarios.models import Firm, User
from veiculos.models import Vehicle, VehicleHistoric


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Firm)
class EmpresaAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VeiculoAdmin(admin.ModelAdmin):
    pass


@admin.register(VehicleHistoric)
class VeiculoHistoricoAdmin(admin.ModelAdmin):
    pass
