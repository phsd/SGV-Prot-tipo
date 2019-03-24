from django.shortcuts import render
from datetime import datetime, timedelta, timezone, date
import datetime
import calendar
from . import models
import pytz
from .forms import FormMaquina
from .forms import FormEstrutura
from .models import Estruturas, Maquina
import math

from django.contrib.auth.decorators import login_required

def somadiasuteis(inicio, numdias):
    diasUteis = 0
    if inicio.hour > 12:
        inicio = inicio + timedelta(days = 1)
    for n in range (0, (numdias * 2)):
        if (inicio + timedelta(n)).weekday() != 6:
            diasUteis = diasUteis + 1
        if diasUteis >= numdias:
            break;
    return (inicio + timedelta(days = n))

def subtrairdatas(start, end):
    if start > end:
        return (abs(start - end).days * (-1))
    else:
        return abs(start - end).days

def subtrairdatasuteis (inicio, fim):
    diasUteis = 0
    if inicio < fim:
        if inicio.hour > 12:
            inicio = inicio + timedelta(days = 1)
        for n in range (0, (abs(inicio - fim).days * 2)):
            if (inicio + timedelta(n)).weekday() != 6:
                diasUteis = diasUteis + 1
            if (inicio + timedelta(n)).replace(hour=23, minute=59, second=59, microsecond=0) >= fim.replace(hour=23, minute=59, second=59, microsecond=0):
                break;
        return (diasUteis)
    elif fim < inicio:
        if fim.hour > 12:
            fim = fim + timedelta(days = 1)
        for n in range (0, (abs(fim - inicio).days * 2)):
            if (fim + timedelta(n)).weekday() != 6:
                diasUteis = diasUteis + 1
            if (fim + timedelta(n)).replace(hour=23, minute=59, second=59, microsecond=0) >= inicio.replace(hour=23, minute=59, second=59, microsecond=0):
                break;
        return (diasUteis)
    else:
        return (0)

def index(request):
    CONST_NUMDIASNOPRAZO = 10
    CONST_NUMDIASFORADOPRAZO = 5

    def numdedomingos(start, end):
        num = 0
        if start < end:
            for n in range(int ((end - start).days) + 1):
                if (start + timedelta(n)).weekday() == 6:
                    num = num + 1
            return num
        else:
            for n in range(int ((start - end).days) + 1):
                if (end + timedelta(n)).weekday() == 6:
                    num = num + 1
            return num

    def buscarCartoesdosProcessos (b, processo):
        busca = models.Estrutura.objects.raw(b)
        gruposCartoesnoPrazo = []
        for x in range(0, CONST_NUMDIASNOPRAZO):
            gruposCartoesnoPrazo.append([])
        gruposCartoesforadoPrazo = []
        for x in range(0, CONST_NUMDIASFORADOPRAZO):
            gruposCartoesforadoPrazo.append([])

        for b in busca:
            dataPrazoMaxProcesso = somadiasuteis(b.dataInicioProcesso, (b.prazoPadraoProcesso + b.prazoProcesso)).replace(hour=23, minute=59, second=59, microsecond=0)#NÃO MEXER
            posicaoGestaoaVista = subtrairdatas(datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0), dataPrazoMaxProcesso)#NÃO MEXER
            if posicaoGestaoaVista >= 0:
                diasNecessarios = subtrairdatasuteis(dataPrazoMaxProcesso, datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0))
            else:
                diasNecessarios = 0
            if processo == "corte":
                diasNecessarios = diasNecessarios + (b.prazopadraocaldsolda + b.prazocaldsolda + b.prazopadraousinagem + b.prazousinagem + b.prazopadraopintura + b.prazopintura)
            elif processo == "caldsolda":
                diasNecessarios = diasNecessarios + (b.prazopadraousinagem + b.prazousinagem + b.prazopadraopintura + b.prazopintura)
            elif processo == "Usinagem":
                diasNecessarios = diasNecessarios + (b.prazopadraopintura + b.prazopintura)
            elif processo == "Pintura":
                diasNecessarios = diasNecessarios

            if datetime.datetime.now() > b.dataInicioProcesso:
                dataEntregaEstimada = somadiasuteis(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), diasNecessarios).replace(hour=23, minute=59, second=0, microsecond=0)
            else:
                dataEntregaEstimada = somadiasuteis(b.dataInicioProcesso, diasNecessarios).replace(hour=23, minute=59, second=0, microsecond=0)
            if posicaoGestaoaVista >= 0:
                diasDisponiveis = subtrairdatasuteis(b.dataEntregaMax.replace(tzinfo=None), dataEntregaEstimada)
            else:
                diasDisponiveis = subtrairdatas(dataEntregaEstimada, b.dataEntregaMax.replace(tzinfo=None)) - 1
            if diasDisponiveis > 0:
                estiloCSSCartaonoPrazodeEntrega = "cartaonoprazodeentrega"
            elif diasDisponiveis > -5:
                estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega1"
            elif diasDisponiveis > -10:
                estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega2"
            else:
                estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega3"

            if posicaoGestaoaVista >= 0 and posicaoGestaoaVista < CONST_NUMDIASNOPRAZO:
                cartoesnoPrazo = gruposCartoesnoPrazo[posicaoGestaoaVista]

                cartoesnoPrazo.append([diasDisponiveis,b, estiloCSSCartaonoPrazodeEntrega])
                gruposCartoesnoPrazo[posicaoGestaoaVista] = cartoesnoPrazo
            elif posicaoGestaoaVista >= CONST_NUMDIASNOPRAZO:
                cartoesnoPrazo = gruposCartoesnoPrazo[-1]
                cartoesnoPrazo.append([diasDisponiveis,b, estiloCSSCartaonoPrazodeEntrega])
                gruposCartoesnoPrazo[-1] = cartoesnoPrazo
            else:
                posicaoGestaoaVista = (posicaoGestaoaVista * (-1))
                if posicaoGestaoaVista < CONST_NUMDIASFORADOPRAZO:
                    cartoesforadoPrazo = gruposCartoesforadoPrazo[posicaoGestaoaVista]
                    cartoesforadoPrazo.append([diasDisponiveis,b, estiloCSSCartaonoPrazodeEntrega])
                    gruposCartoesforadoPrazo[posicaoGestaoaVista] = cartoesforadoPrazo
                else:
                    cartoesforadoPrazo = gruposCartoesforadoPrazo[-1]
                    cartoesforadoPrazo.append([diasDisponiveis,b, estiloCSSCartaonoPrazodeEntrega])
                    gruposCartoesforadoPrazo[-1] = cartoesforadoPrazo

        for x in range(0, CONST_NUMDIASNOPRAZO):
            cartoesnoPrazo = gruposCartoesnoPrazo[x]
            cartoesnoPrazo = sorted(cartoesnoPrazo, key=lambda x: x[0])
            if len(cartoesnoPrazo) < 4:
                for y in range (len(cartoesnoPrazo), 4):
                    cartoesnoPrazo.append(["","empty", ""])
            elif len(cartoesnoPrazo) > 4:
                menorPrazo = 1
                for y in range (3, len(cartoesforadoPrazo)):
                    if cartoesforadoPrazo[y][0] < menorPrazo:
                        menorPrazo = cartoesforadoPrazo[y][0]
                if menorPrazo > 0:
                    estiloCSSCartaonoPrazodeEntrega = "cartaonoprazodeentrega"
                elif menorPrazo > -5:
                    estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega1"
                elif menorPrazo > -10:
                    estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega2"
                else:
                    estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega3"
                cartoesnoPrazo.insert(3, [len(cartoesnoPrazo) - 3, "mais", estiloCSSCartaonoPrazodeEntrega])

            for index, c in enumerate(cartoesnoPrazo):
                c.append(math.ceil((index+1) / 2))
                if ((index+1) % 2 == 0):
                    c.append(2)
                else:
                    c.append(1)
                cartoesnoPrazo[index] = c

            gruposCartoesnoPrazo[x] = cartoesnoPrazo

            if diasnoprazo[x][0].weekday() == 6 and x < (CONST_NUMDIASNOPRAZO - 1):
                gruposCartoesnoPrazo[x] = "domingo"

        for x in range(0, CONST_NUMDIASFORADOPRAZO):
            cartoesforadoPrazo = gruposCartoesforadoPrazo[x]
            cartoesforadoPrazo = sorted(cartoesforadoPrazo, key=lambda x: x[0])
            if len(cartoesforadoPrazo) < 4:
                for y in range (len(cartoesforadoPrazo), 4):
                    cartoesforadoPrazo.append(["empty","empty","empty"])
            elif len(cartoesforadoPrazo) > 4:
                menorPrazo = 1
                for y in range (3, len(cartoesforadoPrazo)):
                    if cartoesforadoPrazo[y][0] < menorPrazo:
                        menorPrazo = cartoesforadoPrazo[y][0]
                if menorPrazo > 0:
                    estiloCSSCartaonoPrazodeEntrega = "cartaonoprazodeentrega"
                elif menorPrazo > -5:
                    estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega1"
                elif menorPrazo > -10:
                    estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega2"
                else:
                    estiloCSSCartaonoPrazodeEntrega = "cartaoforadoprazodeentrega3"
                cartoesforadoPrazo.insert(3, [len(cartoesforadoPrazo) - 3, "mais", estiloCSSCartaonoPrazodeEntrega])

            for index, c in enumerate(cartoesforadoPrazo):
                c.append(math.ceil((index+1) / 2))
                if ((index+1) % 2 == 0):
                    c.append(2)
                else:
                    c.append(1)
                cartoesforadoPrazo[index] = c

            gruposCartoesforadoPrazo[x] = cartoesforadoPrazo


        return (gruposCartoesnoPrazo, gruposCartoesforadoPrazo)

    diasnoprazo = []
    gruposCartoesCortenoPrazo = []
    gruposCartoesCaldSoldanoPrazo = []
    gruposCartoesUsinagemnoPrazo = []
    gruposCartoesPinturanoPrazo = []

    diasUteis = 0
    for x in range(0, CONST_NUMDIASNOPRAZO):
        if (datetime.datetime.today() + timedelta(days=x)).weekday() != 6:
            diasUteis = diasUteis + 1
            diasnoprazo.append([datetime.datetime.today() + timedelta(days=x), diasUteis])
        else:
            diasnoprazo.append([datetime.datetime.today() + timedelta(days=x), "-"])
        if x == CONST_NUMDIASNOPRAZO - 1:
            diasnoprazo[CONST_NUMDIASNOPRAZO - 1] = [datetime.datetime.today() + timedelta(days=x), diasUteis]

        gruposCartoesCortenoPrazo.append([])
        gruposCartoesCaldSoldanoPrazo.append([])
        gruposCartoesUsinagemnoPrazo.append([])
        gruposCartoesPinturanoPrazo.append([])

    diasforadoprazo = []
    gruposCartoesCorteforadoPrazo = []
    gruposCartoesCaldSoldaforadoPrazo = []
    gruposCartoesUsinagemforadoPrazo = []
    gruposCartoesPinturaforadoPrazo = []
    for x in range(0, CONST_NUMDIASFORADOPRAZO):
        diasforadoprazo.append(datetime.datetime.today() - timedelta(days=x+1))
        gruposCartoesCorteforadoPrazo.append([])
        gruposCartoesCaldSoldaforadoPrazo.append([])
        gruposCartoesUsinagemforadoPrazo.append([])
        gruposCartoesPinturaforadoPrazo.append([])

    b = '''SELECT
            telaPrincipal_estrutura.dataInicioManufatura AS dataInicioProcesso,
            telaPrincipal_estruturas.prazopadraocorte As prazoPadraoProcesso, telaPrincipal_estrutura.prazocorte As prazoProcesso,
            telaPrincipal_estruturas.prazopadraocaldsolda, telaPrincipal_estrutura.prazocaldsolda,
            telaPrincipal_estruturas.prazopadraousinagem, telaPrincipal_estrutura.prazousinagem,
            telaPrincipal_estruturas.prazopadraopintura, telaPrincipal_estrutura.prazopintura,
            telaPrincipal_estrutura.id, telaPrincipal_estruturas.nome, telaPrincipal_maquina.serial, telaPrincipal_maquinas.nome,
            telaPrincipal_estrutura.dataEntregaMax, telaPrincipal_estrutura.ordemproducao,
            telaPrincipal_maquina.id As idMaquina
        FROM
            telaPrincipal_estrutura INNER JOIN telaPrincipal_estruturas ON telaPrincipal_estrutura.id_estruturas_id = telaPrincipal_estruturas.id
        INNER JOIN
            telaPrincipal_maquina ON telaPrincipal_estrutura.id_maquina_id = telaPrincipal_maquina.id
        INNER JOIN
            telaPrincipal_maquinas ON telaPrincipal_maquina.id = telaPrincipal_maquinas.id
        WHERE
            telaPrincipal_estrutura.dataBaixaCorte is null;'''
    gruposCartoesCortenoPrazo, gruposCartoesCorteforadoPrazo = buscarCartoesdosProcessos(b, "corte")

    b = '''SELECT
            telaPrincipal_estrutura.dataBaixaCorte As dataInicioProcesso,
            telaPrincipal_estruturas.prazopadraocorte, telaPrincipal_estrutura.prazocorte,
            telaPrincipal_estruturas.prazopadraocaldsolda As prazoPadraoProcesso, telaPrincipal_estrutura.prazocaldsolda As prazoProcesso,
            telaPrincipal_estruturas.prazopadraousinagem, telaPrincipal_estrutura.prazousinagem,
            telaPrincipal_estruturas.prazopadraopintura, telaPrincipal_estrutura.prazopintura,
            telaPrincipal_estrutura.id, telaPrincipal_estruturas.nome, telaPrincipal_maquina.serial, telaPrincipal_maquinas.nome,
            telaPrincipal_estrutura.dataEntregaMax,
            telaPrincipal_estrutura.dataInicioManufatura, telaPrincipal_estrutura.ordemproducao,
            telaPrincipal_maquina.id As idMaquina
        FROM
            telaPrincipal_estrutura INNER JOIN telaPrincipal_estruturas ON telaPrincipal_estrutura.id_estruturas_id = telaPrincipal_estruturas.id
        INNER JOIN
            telaPrincipal_maquina ON telaPrincipal_estrutura.id_maquina_id = telaPrincipal_maquina.id
        INNER JOIN
            telaPrincipal_maquinas ON telaPrincipal_maquina.id = telaPrincipal_maquinas.id
        WHERE
            telaPrincipal_estrutura.dataBaixaCorte is not null
        AND
            telaPrincipal_estrutura.dataBaixaCaldSolda is null;'''
    gruposCartoesCaldSoldanoPrazo, gruposCartoesCaldSoldaforadoPrazo = buscarCartoesdosProcessos(b, "caldsolda")

    b = '''SELECT
            telaPrincipal_estrutura.dataBaixaCaldSolda As dataInicioProcesso,
            telaPrincipal_estruturas.prazopadraocorte, telaPrincipal_estrutura.prazocorte,
            telaPrincipal_estruturas.prazopadraocaldsolda, telaPrincipal_estrutura.prazocaldsolda,
            telaPrincipal_estruturas.prazopadraousinagem As prazoPadraoProcesso, telaPrincipal_estrutura.prazousinagem As prazoProcesso,
            telaPrincipal_estruturas.prazopadraopintura, telaPrincipal_estrutura.prazopintura,
            telaPrincipal_estrutura.id, telaPrincipal_estruturas.nome, telaPrincipal_maquina.serial, telaPrincipal_maquinas.nome,
            telaPrincipal_estrutura.dataEntregaMax,
            telaPrincipal_estrutura.dataInicioManufatura, telaPrincipal_estrutura.ordemproducao,
            telaPrincipal_maquina.id As idMaquina
        FROM
            telaPrincipal_estrutura INNER JOIN telaPrincipal_estruturas ON telaPrincipal_estrutura.id_estruturas_id = telaPrincipal_estruturas.id
        INNER JOIN
            telaPrincipal_maquina ON telaPrincipal_estrutura.id_maquina_id = telaPrincipal_maquina.id
        INNER JOIN
            telaPrincipal_maquinas ON telaPrincipal_maquina.id = telaPrincipal_maquinas.id
        WHERE
            telaPrincipal_estrutura.dataBaixaCaldSolda is not null
        AND
            telaPrincipal_estrutura.dataBaixaUsinagem is null;'''
    gruposCartoesUsinagemnoPrazo, gruposCartoesUsinagemforadoPrazo = buscarCartoesdosProcessos(b, "usinagem")

    b = '''SELECT
            telaPrincipal_estrutura.dataBaixaUsinagem As dataInicioProcesso,
            telaPrincipal_estruturas.prazopadraocorte, telaPrincipal_estrutura.prazocorte,
            telaPrincipal_estruturas.prazopadraocaldsolda, telaPrincipal_estrutura.prazocaldsolda,
            telaPrincipal_estruturas.prazopadraousinagem, telaPrincipal_estrutura.prazousinagem,
            telaPrincipal_estruturas.prazopadraopintura As prazoPadraoProcesso, telaPrincipal_estrutura.prazopintura As prazoProcesso,
            telaPrincipal_estrutura.id, telaPrincipal_estruturas.nome, telaPrincipal_maquina.serial, telaPrincipal_maquinas.nome,
            telaPrincipal_estrutura.dataEntregaMax,
            telaPrincipal_estrutura.dataInicioManufatura, telaPrincipal_estrutura.ordemproducao,
            telaPrincipal_maquina.id As idMaquina
        FROM
            telaPrincipal_estrutura INNER JOIN telaPrincipal_estruturas ON telaPrincipal_estrutura.id_estruturas_id = telaPrincipal_estruturas.id
        INNER JOIN
            telaPrincipal_maquina ON telaPrincipal_estrutura.id_maquina_id = telaPrincipal_maquina.id
        INNER JOIN
            telaPrincipal_maquinas ON telaPrincipal_maquina.id = telaPrincipal_maquinas.id
        WHERE
            telaPrincipal_estrutura.dataBaixaUsinagem is not null
        AND
            telaPrincipal_estrutura.dataBaixaPintura is null;'''
    gruposCartoesPinturanoPrazo, gruposCartoesPinturaforadoPrazo = buscarCartoesdosProcessos(b, "pintura")


    gruposCartoes=[]
    gruposCartoesLinha=[]
    gruposCartoesLinha.append(gruposCartoesCortenoPrazo)
    gruposCartoesLinha.append(gruposCartoesCorteforadoPrazo)
    gruposCartoesLinha.append("Corte")
    gruposCartoes.append(gruposCartoesLinha)

    gruposCartoesLinha=[]
    gruposCartoesLinha.append(gruposCartoesCaldSoldanoPrazo)
    gruposCartoesLinha.append(gruposCartoesCaldSoldaforadoPrazo)
    gruposCartoesLinha.append("Cald/Solda")
    gruposCartoes.append(gruposCartoesLinha)

    gruposCartoesLinha=[]
    gruposCartoesLinha.append(gruposCartoesUsinagemnoPrazo)
    gruposCartoesLinha.append(gruposCartoesUsinagemforadoPrazo)
    gruposCartoesLinha.append("Usinagem")
    gruposCartoes.append(gruposCartoesLinha)

    gruposCartoesLinha=[]
    gruposCartoesLinha.append(gruposCartoesPinturanoPrazo)
    gruposCartoesLinha.append(gruposCartoesPinturaforadoPrazo)
    gruposCartoesLinha.append("Pintura")
    gruposCartoes.append(gruposCartoesLinha)

    contexto = {
        'CONST_NUMDIASNOPRAZO': CONST_NUMDIASNOPRAZO,
        'CONST_NUMDIASFORADOPRAZO': CONST_NUMDIASFORADOPRAZO,
        'diasnoprazo': diasnoprazo,
        'diasforadoprazo': diasforadoprazo,
        'gruposCartoes': gruposCartoes
    }
    return render (request, "telaPrincipal/index.html", contexto)

def maquina(request, id_maquina, id_estrutura):
    def calendProcesso1(inicio, numdias):
        diasProcesso = []
        diasUteis = 0
        if inicio.hour > 12:
            inicio = inicio + timedelta(days = 1)
            inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        for n in range (0, numdias * 2):
            if (inicio + timedelta(n)).weekday() != 6:
                diasUteis = diasUteis + 1
                diasProcesso.append([diasUteis, (inicio + timedelta(n)).replace(hour=23, minute=59, second=59, microsecond=0)])
            else:
                if n > 0:
                    diasProcesso.append(["Dom", (inicio + timedelta(n)).replace(hour=23, minute=59, second=59, microsecond=0)])
            if diasUteis >= numdias:
                break;
        if (inicio + timedelta(n + 1)).weekday() == 6:
            diasProcesso.append(["Dom", (inicio + timedelta(n+1)).replace(hour=23, minute=59, second=59, microsecond=0)])
        return(diasProcesso)

    def calendProcesso2(inicio, fim1, prazoMaxProcesso):
        if fim1 == "agora":
            fim = datetime.datetime.today()
        else:
            fim = fim1
        diasProcesso = []
        diasUteis = 0
        if inicio.hour > 12:
            inicio = inicio + timedelta(days = 1)
            inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        if inicio > fim:
            return (diasProcesso)
        else:
            for n in range(int ((fim.replace(hour=23, minute=0, second=0, microsecond=0) - inicio.replace(hour=0, minute=0, second=0, microsecond=0)).days) + 1):
                if (inicio + timedelta(n)).weekday() != 6:
                    diasUteis = diasUteis + 1
                    if diasUteis <= prazoMaxProcesso:
                        diasProcesso.append([diasUteis, inicio + timedelta(n), "bloconoprazodeentrega", "", ""])
                    else:
                        diasProcesso.append([diasUteis, inicio + timedelta(n), "blocoforadoprazodeentrega", "", ""])
                else:
                    if n >= 0:
                        diasProcesso.append(["Dom", inicio + timedelta(n), "domingo", "", ""])
            if fim.hour <= 12 and fim1 != "agora":
                diasProcesso.pop()
                diasProcesso[-1][3] = "2em1"
                diasProcesso[-1][4] = fim
            else:
                diasProcesso[-1][1] = fim
            return(diasProcesso)

    b = '''SELECT
            telaPrincipal_estrutura.dataBaixaUsinagem,
            telaPrincipal_estruturas.prazopadraocorte, telaPrincipal_estrutura.prazocorte,
            telaPrincipal_estruturas.prazopadraocaldsolda, telaPrincipal_estrutura.prazocaldsolda,
            telaPrincipal_estruturas.prazopadraousinagem, telaPrincipal_estrutura.prazousinagem,
            telaPrincipal_estruturas.prazopadraopintura , telaPrincipal_estrutura.prazopintura,
            telaPrincipal_estrutura.id, telaPrincipal_estruturas.nome As nomeestrutura, telaPrincipal_maquina.serial, telaPrincipal_maquinas.nome As nomemaquina,
            telaPrincipal_estrutura.dataEntregaMax,
            telaPrincipal_estrutura.dataInicioManufatura, telaPrincipal_estrutura.ordemproducao
        FROM
            telaPrincipal_estrutura
        INNER JOIN
            telaPrincipal_estruturas ON telaPrincipal_estrutura.id_estruturas_id = telaPrincipal_estruturas.id
        INNER JOIN
            telaPrincipal_maquina ON telaPrincipal_estrutura.id_maquina_id = telaPrincipal_maquina.id
        INNER JOIN
            telaPrincipal_maquinas ON telaPrincipal_maquina.id = telaPrincipal_maquinas.id
        WHERE
            telaPrincipal_estrutura.id_maquina_id = '''+ id_maquina +''';'''
    busca = models.Estrutura.objects.raw(b)
    estruturas = []
    maquina = ['', '', '']
    for b in busca:
        estrutura = []
        maquina[0] = b.serial
        maquina[1] = b.nomemaquina
        estrutura.append(b.ordemproducao) #0
        estrutura.append(b.nomeestrutura) #1
        diasProcesso = calendProcesso1(b.dataInicioManufatura, b.prazopadraocorte + b.prazocorte)
        estrutura.append(len(diasProcesso)) #2
        estrutura.append(diasProcesso) #3

        diasProcesso = calendProcesso1(diasProcesso[-1][1], b.prazopadraocaldsolda + b.prazocaldsolda)
        estrutura.append(len(diasProcesso)) #4
        estrutura.append(diasProcesso) #5

        diasProcesso = calendProcesso1(diasProcesso[-1][1], b.prazopadraousinagem + b.prazousinagem)
        estrutura.append(len(diasProcesso)) #6
        estrutura.append(diasProcesso) #7

        diasProcesso = calendProcesso1(diasProcesso[-1][1], b.prazopadraopintura + b.prazopintura)
        estrutura.append(len(diasProcesso)) #8
        estrutura.append(diasProcesso) #9
        diasProcesso = calendProcesso1(diasProcesso[-1][1], subtrairdatasuteis(diasProcesso[-1][1], b.dataEntregaMax))
        estrutura.append(len(diasProcesso)) #10
        estrutura.append(diasProcesso) #11

        if (b.dataBaixaCorte is not None):
            diasProcesso = calendProcesso2(b.dataInicioManufatura, b.dataBaixaCorte, b.prazopadraocorte + b.prazocorte)
            estrutura.append(len(diasProcesso)) #12 corte
            estrutura.append(diasProcesso) #13 corte
            if (b.dataBaixaCaldSolda is not None):
                diasProcesso = calendProcesso2(b.dataBaixaCorte, b.dataBaixaCaldSolda, b.prazopadraocaldsolda + b.prazocaldsolda)
                estrutura.append(len(diasProcesso)) #14 cald/solda
                estrutura.append(diasProcesso) #15 cald/solda
                if (b.dataBaixaUsinagem is not None):
                    diasProcesso = calendProcesso2(b.dataBaixaCaldSolda, b.dataBaixaUsinagem, b.prazopadraousinagem + b.prazousinagem)
                    estrutura.append(len(diasProcesso)) #16 usinagem
                    estrutura.append(diasProcesso) #17 usinagem
                    if (b.dataBaixaPintura is not None):
                        diasProcesso = calendProcesso2(b.dataBaixaUsinagem, b.dataBaixaPintura, b.prazopadraopintura + b.prazopintura)
                        estrutura.append(len(diasProcesso)) #18 pintura
                        estrutura.append(diasProcesso) #19 pintura
                    else:
                        diasProcesso = calendProcesso2(b.dataBaixaUsinagem, "agora", b.prazopadraopintura + b.prazopintura)
                        estrutura.append(len(diasProcesso)) #18 pintura
                        estrutura.append(diasProcesso) #19 pintura
                else:
                    diasProcesso = calendProcesso2(b.dataBaixaCaldSolda, "agora", b.prazopadraousinagem + b.prazousinagem)
                    estrutura.append(len(diasProcesso)) #16 usinagem
                    estrutura.append(diasProcesso) #17 usinagem
                    estrutura.append("") #18 pintura
                    estrutura.append("") #19 pintura
            else:
                diasProcesso = calendProcesso2(b.dataBaixaCorte, "agora", b.prazopadraocaldsolda + b.prazocaldsolda)
                estrutura.append(len(diasProcesso)) #14 cald/solda
                estrutura.append(diasProcesso) #15 cald/solda
                estrutura.append("") #16 usinagem
                estrutura.append("") #17 usinagem
                estrutura.append("") #18 pintura
                estrutura.append("") #19 pintura
        else:
            diasProcesso = calendProcesso2(b.dataInicioManufatura, "agora", b.prazopadraocorte + b.prazocorte)
            estrutura.append(len(diasProcesso)) #12 corte
            estrutura.append(diasProcesso) #13 corte
            estrutura.append("") #14 cald/solda
            estrutura.append("") #15 cald/solda
            estrutura.append("") #16 usinagem
            estrutura.append("") #17 usinagem
            estrutura.append("") #18 pintura
            estrutura.append("") #19 pintura

        if (str(id_estrutura) == str(b.id)):
            estrutura.append("estruturadestaque")
        else:
            estrutura.append("")

        estruturas.append(estrutura)

    contexto = {
        'maquina': maquina,
        'estruturas': estruturas
    }
    return render (request, "telaPrincipal/maquina.html", contexto)

@login_required
def formularioMaquina(request):
    if request.method == "POST":
        form = FormMaquina(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
        form = FormMaquina()
        return render(request, 'telaPrincipal/formMaquina.html', {'form': form})
    else:
        form = FormMaquina()
        return render(request, 'telaPrincipal/formMaquina.html', {'form': form})

@login_required
def formularioEstrutura(request):
    if request.method == "POST":
        form = FormEstrutura(request.POST)
        if form.is_valid():
            print ("dadsa")
            post = form.save(commit=False)
            post.save()
            form = FormEstrutura()
        return render(request, 'telaPrincipal/formEstrutura.html', {'form': form})
    else:
        form = FormEstrutura()
        return render(request, 'telaPrincipal/formEstrutura.html', {'form': form})

def carregarEstruturas(request):
    idBusca = request.GET.get('id_maquina')
    #print(idBusca)
    #maquina = Maquina.objects.filter(id=idBusca)
    #for m in maquina:
    #    estruturas = Estruturas.objects.filter(id_maquinas_id=m.id).order_by('nome')
    #for e in estruturas:
    #    print (e)

    b = '''SELECT
            telaPrincipal_estruturas.id, telaPrincipal_estruturas.nome
        FROM
            telaPrincipal_estruturas
        INNER JOIN
            telaPrincipal_maquinas ON telaPrincipal_estruturas.id_maquinas_id = telaPrincipal_maquinas.id
        INNER JOIN
            telaPrincipal_maquina ON telaPrincipal_maquinas.id = telaPrincipal_maquina.id_maquinas_id
        WHERE
            telaPrincipal_maquina.id = '''+ idBusca +''';'''
    busca = models.Estrutura.objects.raw(b)
    return render(request, 'telaPrincipal/estruturas_dropdown_list_options.html', {'estruturas': busca})

def carregarPrazosEstrutura(request):
    id_estrutura = request.GET.get('id_estrutura')
    if id_estrutura != "":
        prazos = Estruturas.objects.filter(id = id_estrutura)
        return render(request, 'telaPrincipal/prazosEstrutura.json', {'prazos': prazos})
    else:
        return render(request, 'telaPrincipal/prazosEstrutura.json', {'prazos': "empty"})
