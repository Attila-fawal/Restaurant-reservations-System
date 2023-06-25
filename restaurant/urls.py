"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservations import views
from reservations.views import CancelReservationView, ReservationCreateView, TableListView
from reservations.views import UserLoginView, UserRegisterView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tables/', TableListView.as_view(), name='table_list'),
    path('reservation/new/', ReservationCreateView.as_view(), name='reservation_new'),
    path('reservation/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/list/', views.reservation_list, name='reservation_list'),
    path('reservation/cancel/<int:pk>/', CancelReservationView.as_view(), name='reservation_cancel'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('reservation/list/', views.reservation_list, name='reservation_list'),


]

