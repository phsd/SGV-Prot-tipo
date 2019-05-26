from django.contrib import admin

# Register your models here.
from .models import Maquinas, Maquina, Estruturas, Estrutura, Setores, Locais, HourlyScheduleManagement, HourlyScheduleManagementRealizado, HSMEmProcesso

admin.site.register(Maquinas)
admin.site.register(Maquina)
admin.site.register(Estruturas)
admin.site.register(Estrutura)
admin.site.register(Setores)
admin.site.register(Locais)
admin.site.register(HourlyScheduleManagement)
admin.site.register(HourlyScheduleManagementRealizado)
admin.site.register(HSMEmProcesso)
