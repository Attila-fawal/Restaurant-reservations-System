from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Table, Reservation

def home(request):
    return render(request, 'home.html')

class TableListView(ListView):
    model = Table
    context_object_name = 'tables'  # This is the context variable name in the template
    template_name = 'tables.html'

class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['customer', 'date', 'time', 'guests']
    template_name = 'reservation_form.html'
