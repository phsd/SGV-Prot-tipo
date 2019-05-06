from django import forms
from .models import Maquina, Maquinas
from .models import Estrutura
from .models import Estruturas
from .models import HourlyScheduleManagement
from .models import Locais

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
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-group'

        self.fields['prazocorte'].initial = 0
        self.fields['prazocaldsolda'].initial = 0
        self.fields['prazousinagem'].initial = 0
        self.fields['prazopintura'].initial = 0

        self.fields['id_estruturas'].queryset = Estruturas.objects.none()


        if 'id_maquina' in self.data:
            try:
                idBusca = int(self.data.get('id_maquina'))
                idMaquina = Maquina.objects.filter(id=idBusca)
                for idm in idMaquina:
                    print (idm.id_maquinas.id)
                    self.fields['id_estruturas'].queryset = Estruturas.objects.filter(id_maquinas=idm.id_maquinas.id)
                    break;
            except (ValueError, TypeError):
                print ("aqui4")
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            print ("aqui5")
            self.fields['id_estruturas'].queryset = self.instance.id_maquina.id_estruturas_set

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

LOCAISLIST = []


MES = [
    ('1', 'Janeiro'),
    ('2', 'Fevereiro'),
    ('3', 'Março'),
    ('4', 'Abril'),
    ('5', 'Maio'),
    ('6', 'Junho'),
    ('7', 'Julho'),
    ('8', 'Agosto'),
    ('9', 'Setembro'),
    ('10', 'Outubro'),
    ('11', 'Novembro'),
    ('12', 'Dezembro'),
    ]
ANO = [
    ('2019', '2019'),
    ('2020', '2020'),
    ]
class FormHourlySchedManag1(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FormHourlySchedManag1, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-group'

        self.fields['id_local'].queryset = Estruturas.objects.none()

    id_local= forms.CharField(label='Local:', widget=forms.Select(choices=LOCAISLIST))
    mes= forms.CharField(label='Mês:', widget=forms.Select(choices=MES))
    ano= forms.CharField(label='Ano:', widget=forms.Select(choices=ANO))

class FormScheduleManagement(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormScheduleManagement, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-group'

        self.fields['id_estrutura'].queryset = Estruturas.objects.none()
        b = '''SELECT
                telaPrincipal_estrutura.dataBaixaCaldSolda As dataInicioProcesso,
                telaPrincipal_estruturas.prazopadraocorte, telaPrincipal_estrutura.prazocorte,
                telaPrincipal_estruturas.prazopadraocaldsolda, telaPrincipal_estrutura.prazocaldsolda,
                telaPrincipal_estruturas.prazopadraousinagem As prazoPadraoProcesso, telaPrincipal_estrutura.prazousinagem As prazoProcesso,
                telaPrincipal_estruturas.prazopadraopintura, telaPrincipal_estrutura.prazopintura,
                telaPrincipal_estrutura.id, telaPrincipal_estruturas.nome As nomeEstrutura, telaPrincipal_maquina.serial, telaPrincipal_maquinas.nome As nomeMaquina,
                telaPrincipal_estrutura.dataEntregaMax,
                telaPrincipal_estrutura.dataInicioManufatura, telaPrincipal_estrutura.ordemproducao,
                telaPrincipal_maquina.id As idMaquina
            FROM
                telaPrincipal_estrutura
            INNER JOIN
                telaPrincipal_estruturas ON telaPrincipal_estrutura.id_estruturas_id = telaPrincipal_estruturas.id
            INNER JOIN
                telaPrincipal_maquina ON telaPrincipal_estrutura.id_maquina_id = telaPrincipal_maquina.id
            INNER JOIN
                telaPrincipal_maquinas ON telaPrincipal_maquina.id_maquinas_id = telaPrincipal_maquinas.id
            WHERE
                telaPrincipal_estrutura.dataBaixaCaldSolda is not null
            AND
                telaPrincipal_estrutura.dataBaixaUsinagem is null;'''
        busca = Estrutura.objects.raw(b)

        for b in busca:
            self.fields['id_estrutura'].choices = \
                list(self.fields['id_estrutura'].choices) + [(b.id, "MO: " + b.ordemproducao + " - " + b.nomeEstrutura + " " + b.nomeMaquina)]

        if 'id_estrutura' in self.data:
            try:
                idBusca = int(self.data.get('id_estrutura'))
                print(idBusca)
                self.fields['id_estrutura'].queryset = Estrutura.objects.filter(id=idBusca)
            except (ValueError, TypeError):
                print ("aqui4")
                pass  # invalid input from the client; ignore and fallback to empty City queryset




    class Meta:
        model = HourlyScheduleManagement
        fields = ('id_local', 'id_estrutura', 'diaeHoraEntrada', 'diaeHoraSaida')
        labels = {
            'id_local': 'Local:', 'id_estrutura': 'Estrutura:', 'diaeHoraEntrada': 'Início:', 'diaeHoraSaida': 'Fim:',
        }
