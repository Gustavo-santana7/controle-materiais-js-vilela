from django.contrib import admin
from django.urls import path

from materiais import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('materiais/', views.materiais, name='materiais'),
    path(
        'movimentacoes/',
        views.movimentacoes,
        name='movimentacoes'
    ),
    path(
        'consulta-estoque/',
        views.consulta_estoque,
        name='consulta_estoque'
    ),
    path('admin/', admin.site.urls),
]