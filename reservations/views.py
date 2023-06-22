from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Table, Reservation
from .forms import ReservationForm

def reservation_new(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})

def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save()
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation_form.html', {'form': form})

def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

def reservation_list(request):
    reservations = Reservation.objects.filter(customer=request.user.customer)
    return render(request, 'reservation_list.html', {'reservations': reservations})

def home(request):
    return render(request, 'home.html')

class TableListView(ListView):
    model = Table
    context_object_name = 'tables'
    template_name = 'tables.html'


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)


class CancelReservationView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=kwargs.get('pk'))
        reservation.cancel()
        return HttpResponseRedirect(reverse('home'))
