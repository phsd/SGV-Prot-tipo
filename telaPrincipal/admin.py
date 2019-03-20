from django.contrib import admin

# Register your models here.
from .models import Estrutura
from .models import Maquina

admin.site.register(Estrutura)
