from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('equipamientos/listar/', views.listar_equipamientos, name='listar_equipamientos'),
    path('equipamientos/agregar/', views.agregar_equipamiento, name='agregar_equipamiento'),
    path('equipamientos/editar/<int:id>/', views.editar_equipamiento, name='editar_equipamiento'),
    path('equipamientos/eliminar/<int:id>/', views.eliminar_equipamiento, name='eliminar_equipamiento'),
    path('equipamientos/detalle/<int:pk>/', views.detalle_equipamiento, name='detalle_equipamiento'),
]
