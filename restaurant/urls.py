from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from reservations import views
from reservations.views import UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tables/', views.reservation_list, name='tables'),
    path('reservation/new/', views.ReservationCreateView.as_view(), name='reservation_new'),
    path('reservation/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/list/', views.reservation_list, name='reservation_list'),
    path('reservation/cancel/<int:pk>/', views.CancelReservationView.as_view(), name='reservation_cancel'),
    path('login/', auth_views.LoginView.as_view(template_name='templates/registration/login.html'), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create_sample_menu/', views.create_sample_menu, name='create_sample_menu'),
]
