from django.urls import path, include

from .views import OrdersList, AuthenticateUser


urlpatterns = [
    path('login', AuthenticateUser.as_view()),
    path('orders', OrdersList.as_view()),
]