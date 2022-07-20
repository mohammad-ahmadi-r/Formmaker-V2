from django.urls import path
from . import views

app_name= 'atent'

urlpatterns = [
    path("register/" , views.register , name = 'register'),
    path("login/" , views.login_view , name = 'login'),
    path("logout/" , views.logout_view , name = 'logout'),
    path("forgot-password/", views.forgot_password , name = 'forgot_password'),
    path("reset-password/<str:token>/", views.reset_password , name = 'reset_password')
]
