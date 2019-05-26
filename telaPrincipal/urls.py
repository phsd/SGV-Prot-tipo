from . import views
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

app_name = 'telaPrincipal'

urlpatterns = [
    url(r'^$', view=views.index, name='index'),
    url(r'^maquina/(?P<id_maquina>[-\w]+)/(?P<id_estrutura>[-\w]+)/$', view=views.maquina, name='urlMaquina'),
    url(r'^formMaquina', views.formularioMaquina, name='urlFormMaquina'),
    url(r'^FormEstrutura', views.formularioEstrutura, name='urlFormEstrutura'),
    url(r'^ajax/carregarEstruturas/', views.carregarEstruturas, name='ajaxCarregarEstruturas'),
    url(r'^ajax/carregarPrazosEstrutura/', views.carregarPrazosEstrutura, name='ajaxCarregarPrazosEstrutura'),
    url('accounts/login/', auth_views.LoginView.as_view(), name='loginForm'),
    url('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^HourlyScheduleManagement1', views.hourlySchedManag1, name='urlHourlySchedManag1'),
    url(r'^HourlyScheduleManagement2/(?P<local>[-\w]+)/(?P<mes>[-\w]+)/(?P<ano>[-\w]+)/$', views.hourlySchedManag2, name='urlHourlySchedManag2'),
    url(r'^formHourlyScheduleManagement', views.formularioHourlySchedManag, name='urlFormHourlySchedManag'),
    url(r'^hsm', views.formularioHourlySchedManagAdd, name='urlFormHourlySchedManagAdd'),

    url(r'^ajax/carEstrProcHSM/', views.carregarEstrProcHSM, name='ajaxCarEstrProcHSM'),

    url(r'^bc', views.baixarCartao, name='urlBaixarCartao'),
    url(r'^cb/(?P<processo>[-\w]+)/(?P<idestrutura>[-\w]+)/$', views.baixarCartaoSalvar, name='urlBaixarCartaoSalvar'),
]
