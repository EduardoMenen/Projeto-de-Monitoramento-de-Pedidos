from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('enviar-pedido/', views.enviar_pedido_form),
]