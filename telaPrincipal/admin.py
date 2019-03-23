from django.contrib import admin

# Register your models here.
from .models import Maquinas, Maquina, Estruturas, Estrutura

class MaquinasAdmin(admin.ModelAdmin):
    list_display = ['nome', 'areaNegocio']

admin.site.register(Maquinas, MaquinasAdmin)
admin.site.register(Maquina)
admin.site.register(Estruturas)
admin.site.register(Estrutura)
