from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('login',views.login),
    path('trips/new', views.new),
    path('add_new', views.add_new),
    path('logout', views.logout),
    path('trips/<int:id>', views.trips),
    path('trips/edit/<int:id>', views.edit),
    path('edit_trip/<int:id>', views.edit_trip),
    path('join/<int:id>', views.join),
    path('remove/<int:id>', views.remove),
    path('cancel/<int:id>', views.cancel)
]