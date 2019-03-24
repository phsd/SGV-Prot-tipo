from django import forms
from .models import Maquina
from .models import Estrutura
from .models import Estruturas
from tempus_dominus.widgets import DateTimePicker

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
class FormMaquina(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormMaquina, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-group'

    class Meta:
        model = Maquina
        fields = ('id_maquinas', 'serial')
        labels = {
            'id_maquinas': 'Modelo da máquina/Pacote:', 'serial': 'Número de série:',
        }

class FormEstrutura(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEstrutura, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-group'

        self.fields['prazocorte'].initial = 0
        self.fields['prazocaldsolda'].initial = 0
        self.fields['prazousinagem'].initial = 0
        self.fields['prazopintura'].initial = 0

        self.fields['id_estruturas'].queryset = Estruturas.objects.none()
        if 'id_maquina' in self.data:
            try:
                idMaquina = int(self.data.get('id_maquina'))
                self.fields['id_estruturas'].queryset = Estruturas.objects.filter(id_maquinas=idMaquina).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['id_estruturas'].queryset = self.instance.id_maquina.id_estruturas_set.order_by('nome')

    class Meta:
        model = Estrutura
        fields = ('id_maquina', 'id_estruturas', 'ordemproducao', 'dataInicioManufatura', 'dataEntregaMax', 'prazocorte', 'prazocaldsolda', 'prazousinagem', 'prazopintura')
        labels = {
            'id_maquina': 'Modelo e SN da máquina:', 'id_estruturas': 'Estrutura:',
            'ordemproducao': 'Ordem de produção:', 'dataInicioManufatura': 'Início da produção:',
            'dataEntregaMax': 'Data de entrega max:', 'prazocorte': 'Dias adicionais para Corte:',
            'prazocaldsolda': 'Dias para Cald/Solda:', 'prazousinagem': 'Dias para Usinagem:',
            'prazopintura': 'Dias para Pintura:',
        }

        widgets = {
            'dataInicioManufatura': DateTimePicker(
                options={
                    'useCurrent': True,
                    'collapse': False
                }
            ),
            'dataEntregaMax': DateTimePicker(
                options={
                    'useCurrent': True,
                    'collapse': False
                }
            ),
        }
