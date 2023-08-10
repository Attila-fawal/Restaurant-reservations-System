from django.urls import path
from . import views

urlpatterns = [
    path('reservation/edit/<int:pk>/', views.ReservationUpdateView.as_view(), name='edit_reservation'),
]
