from django.urls import path
from . import views
urlpatterns = [
    path('crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('lista/', views.CotizacionListView.as_view(), name='lista_cotizaciones'),
    path('detalle/<int:pk>/', views.CotizacionDetailView.as_view(), name='detalle_cotizacion'),
    path('editar/<int:pk>/', views.CotizacionUpdateView.as_view(), name='editar_cotizacion'),
]