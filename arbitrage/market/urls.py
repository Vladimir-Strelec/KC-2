from django.urls import path
from .views import arbitrage_page

urlpatterns = [
    path('', arbitrage_page, name='arbitrage'),
]
