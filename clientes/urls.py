from django.urls import path

from . import views

urlpatterns = [
    path('', views.crear_cliente, name='clientes_crear'),
]
