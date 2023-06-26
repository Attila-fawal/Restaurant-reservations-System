from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Table, Reservation, ReservationTable
from .forms import ReservationForm
from math import ceil
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages


class TableListView(ListView):
    model = Table
    context_object_name = 'tables'
    template_name = 'tables.html'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.customer_user = self.request.user

        num_guests = reservation.guests

        if num_guests < 1:
            form.add_error(None, 'Reservation must be for at least one person.')
            return self.form_invalid(form)
        
        num_tables_required = ceil(num_guests / 2)
        available_tables = Table.objects.filter(is_reserved=False)[:num_tables_required]

        if len(available_tables) < num_tables_required:
            form.add_error(None, 'Not enough tables are available at the moment. Please try again later.')
            return self.form_invalid(form)
        else:
            reservation.save()

            for table in available_tables:
                table.is_reserved = True
                table.save()
                ReservationTable.objects.create(reservation=reservation, table=table)
            
            messages.success(self.request, f'Reservation made successfully. Reservation ID: {reservation.pk}. We look forward to serving you!')

            return redirect('table_list')


class CancelReservationView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=kwargs.get('pk'))
        reservation.cancel()
        return HttpResponseRedirect(reverse('home'))


def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation_detail.html', {'reservation': reservation})


def reservation_list(request):
    reservations = Reservation.objects.filter(customer_user=request.user)
    return render(request, 'reservation_list.html', {'reservations': reservations})


def home(request):
    return render(request, 'home.html')


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


