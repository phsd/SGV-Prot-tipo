from django.contrib import admin

# Register your models here.
from .models import Maquinas, Maquina, Estruturas, Estrutura

admin.site.register(Maquinas)
admin.site.register(Maquina)
admin.site.register(Estruturas)
admin.site.register(Estrutura)
