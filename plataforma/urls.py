from django.urls import path
from . import views


urlpatterns = [
    path('pacientes/', views.paciente, name='paciente_url'),
    path('dados_pacientes/', views.dados_pacientes_listar, name='dados_pacientes_listar_url'),
    path('dados_paciente/<str:id>/', views.dados_paciente, name='dados_paciente_url'),
    path('grafico_peso/<str:id>/', views.grafico_peso, name='grafico_peso_url'),
    path('plano_alimentar_listar/', views.plano_alimentar_listar, name='plano_alimentar_listar_url'),
    path('plano_alimentar/<str:id>/', views.plano_alimentar, name='plano_alimentar_url'),
    path('refeicao/<str:id_paciente>/', views.refeicao, name='refeicao_url'),
    path('opcao/<str:id_paciente>/', views.opcao, name='opcao_url'),
    path('pdf/<str:id>/', views.pdf, name='pdf_url'),
]
