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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from reservations import views
from reservations.views import UserRegisterView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tables/', views.TableListView.as_view(), name='table_list'),
    path('reservation/new/', views.ReservationCreateView.as_view(), name='reservation_new'),
    path('reservation/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/list/', views.reservation_list, name='reservation_list'),
    path('reservation/cancel/<int:pk>/', views.CancelReservationView.as_view(), name='reservation_cancel'),
    path('login/', auth_views.LoginView.as_view(template_name='templates/registration/login.html'), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create_sample_menu/', views.create_sample_menu, name='create_sample_menu'),
    path('register/', UserRegisterView.as_view(), name='register'),  

]
