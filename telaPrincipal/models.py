from django.db import models

# Create your models here.
class Maquinas (models.Model):
    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    areaNegocio = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    def __str__(self):
        return self.nome

class Estruturas (models.Model):
    id_maquinas = models.ForeignKey('Maquinas', on_delete=models.PROTECT)
    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    prazopadraocorte = models.IntegerField(
        null=False, blank=False
    )
    prazopadraocaldsolda = models.IntegerField(
        null=False, blank=False
    )
    prazopadraousinagem = models.IntegerField(
        null=False, blank=False
    )
    prazopadraopintura = models.IntegerField(
        null=False, blank=False
    )
    def __str__(self):
        return self.nome

class Maquina (models.Model):
    id_maquinas = models.ForeignKey('Maquinas', on_delete=models.PROTECT)
    serial = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    def __str__(self):
        return (str(self.id_maquinas.nome) + " - SN: " + str(self.serial))

class Estrutura (models.Model):
    id_maquina = models.ForeignKey('Maquina', on_delete=models.PROTECT)
    id_estruturas = models.ForeignKey('Estruturas', on_delete=models.PROTECT)
    ordemproducao = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    prazocorte = models.IntegerField(
        null=False, blank=False
    )
    prazocaldsolda = models.IntegerField(
        null=False, blank=False
    )
    prazousinagem = models.IntegerField(
        null=False, blank=False
    )
    prazopintura = models.IntegerField(
        null=False, blank=False
    )
    dataEntregaMax = models.DateTimeField(null=False)
    dataEntradaSistema = models.DateTimeField(auto_now_add=True)
    dataInicioManufatura = models.DateTimeField(null=False)
    dataBaixaCorte = models.DateTimeField(null=True)
    dataBaixaCaldSolda = models.DateTimeField(null=True)
    dataBaixaUsinagem = models.DateTimeField(null=True)
    dataBaixaPintura = models.DateTimeField(null=True)
    dataConfirmEntrega = models.DateTimeField(null=True)
