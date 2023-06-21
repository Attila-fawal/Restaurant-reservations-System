from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Table, Reservation
from .forms import ReservationForm


def home(request):
    return render(request, 'home.html')


class TableListView(ListView):
    model = Table
    context_object_name = 'tables'
    template_name = 'tables.html'


class CancelReservationView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the reservation
        reservation = Reservation.objects.get(pk=kwargs.get('pk'))

        # Cancel the reservation
        reservation.cancel()

        # Redirect to the home page (or wherever you want to redirect after cancellation)
        return HttpResponseRedirect(reverse('home'))


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = '/reservation/new/'


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)  # Temporarily save reservation without committing to db
            tables = form.cleaned_data.get('tables')
            # Save tables after reservation instance is created
            reservation.save()
            reservation.tables.set(tables)
            reservation.save()
            return redirect('/reservation/new/')
        else:
            # If form is invalid, re-render the form with error messages
            return render(request, 'reservation_form.html', {'form': form})
    else:
        form = ReservationForm()
        return render(request, 'reservation_form.html', {'form': form})

