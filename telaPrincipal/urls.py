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
    url('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='loginForm'),
    url('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
