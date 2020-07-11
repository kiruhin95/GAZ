from django.urls import path, re_path
from . import views

app_name = "administration"

urlpatterns = [
    path('', views.index),
    path('reg/', views.user_reg),
]
