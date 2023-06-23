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
            reservation = form.save(commit=False)
            available_tables = Table.objects.filter(capacity__gte=reservation.capacity)
            if available_tables.exists():
                assigned_table = available_tables.first()
                reservation.table = assigned_table
                reservation.save()
                return redirect('reservation_detail', pk=reservation.pk)
            else:
                form.add_error(None, 'No tables are available at the moment. Please try again later.')
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
        reservation = form.save(commit=False)
        reservation.customer_user = self.request.user
        available_tables = Table.objects.filter(capacity__gte=reservation.capacity)
        if available_tables.exists():
            assigned_table = available_tables.first()
            reservation.table = assigned_table
            reservation.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'No tables are available at the moment. Please try again later.')
            return self.form_invalid(form)


class CancelReservationView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=kwargs.get('pk'))
        reservation.cancel()
        return HttpResponseRedirect(reverse('home'))
