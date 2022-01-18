from django.urls import path
from .views import calculate, get_correlation, custom_login, custom_logout

urlpatterns = [
    path('calculate/', calculate),
    path('correlation/', get_correlation),
    path('login/', custom_login),
    path('logout/', custom_logout),
]
