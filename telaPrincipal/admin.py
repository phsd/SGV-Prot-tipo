from django.contrib import admin

# Register your models here.
from .models import Maquinas
from .models import Estruturas
from .models import Estrutura
from .models import Maquina

admin.site.register(Maquinas)
admin.site.register(Estruturas)
admin.site.register(Maquina)
admin.site.register(Estrutura)
