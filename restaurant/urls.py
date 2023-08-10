from .views import handler404
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from reservations import views
from reservations.views import (
    UserRegisterView, change_password, update_profile
)
from django.urls import include
from reservations.views import DeleteAccountView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tables/', views.reservation_list, name='tables'),
    path(
        'reservation/new/',
        views.ReservationCreateView.as_view(),
        name='reservation_new'
    ),
    path(
        'reservation/<int:pk>/',
        views.reservation_detail,
        name='reservation_detail'
    ),
    path('reservation/list/', views.reservation_list, name='reservation_list'),
    path(
        'reservation/cancel/<int:pk>/',
        views.CancelReservationView.as_view(),
        name='reservation_cancel'
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='templates/registration/login.html'
        ),
        name='login'
    ),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),
    path('profile/', update_profile, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('reservations/', include('reservations.urls')),


]

handler404 = 'restaurant.views.handler404'
