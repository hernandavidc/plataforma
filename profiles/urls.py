from django.urls import path, include
from .views import checkClient, ClienteListView, ClienteDetailView, homeView

profiles_patterns = ([
    #path('', ClienteListView.as_view(), name='cliente_list'),
    path('inicio/', homeView.as_view(), name='inicio'),
    path('checkclient/<int:cc>/', checkClient, name='check_client'),
], "profiles")
