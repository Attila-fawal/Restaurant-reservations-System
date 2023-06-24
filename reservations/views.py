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
            reservation.capacity = 1  # This could be an input from the user.
            if reservation.capacity < 1:
                form.add_error(None, 'Reservation must be for at least one person.')
                return render(request, 'reservation_form.html', {'form': form})
            num_tables = -(-reservation.capacity // 2)  # Equivalent to rounding up.
            available_tables = Table.objects.filter(capacity__gte=2)[:num_tables]
            if len(available_tables) < num_tables:
                form.add_error(None, 'Not enough tables are available at the moment. Please try again later.')
            else:
                reservation.save()  # Need to save reservation before linking it to tables.
                for table in available_tables:
                    ReservationTable.objects.create(reservation=reservation, table=table)
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

    class ReservationCreateView(CreateView):
        model = Reservation
    fields = ['guests', 'date', 'time']
    template_name = 'reservation_form.html'

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.customer_user = self.request.user
        reservation.capacity = 1  # Assuming this is the number of guests.

        num_guests = reservation.guests

        if num_guests < 1:
            form.add_error(None, 'Reservation must be for at least one person.')
            return self.form_invalid(form)
        
        # Calculate required tables.
        num_tables_required = ceil(num_guests / 2)

        # Fetch available tables
        available_tables = Table.objects.filter(is_reserved=False)[:num_tables_required]

        if len(available_tables) < num_tables_required:
            form.add_error(None, 'Not enough tables are available at the moment. Please try again later.')
            return self.form_invalid(form)
        else:
            reservation.save()  # Save reservation before linking it to tables.

            # Reserve the tables
            for table in available_tables:
                table.is_reserved = True
                table.save()
                ReservationTable.objects.create(reservation=reservation, table=table)
            
            # Add success message
            messages.success(self.request, f'Reservation made successfully. Reservation ID: {reservation.pk}. We look forward to serving you!')

            return redirect('tables')


class CancelReservationView(View):
    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=kwargs.get('pk'))
        reservation.cancel()
        return HttpResponseRedirect(reverse('home'))
