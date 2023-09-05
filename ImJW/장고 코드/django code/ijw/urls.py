from django.urls import path
from . import views

urlpatterns = [
    path('ijw/', views.predict_view, name='predict'),
    path('get_sigun/', views.get_sigun, name='get_sigun'),
    path('get_eup/', views.get_eup, name='get_eup'),
    path('get_ri/', views.get_ri, name='get_ri'),
]