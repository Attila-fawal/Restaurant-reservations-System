from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Reservation, Table
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ReservationForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class TableListView(ListView):
    model = Table
    template_name = 'table_list.html'

class ReservationCreateView(SuccessMessageMixin, CreateView):
    model = Reservation
    fields = ['date', 'time', 'guests']
    template_name = 'reservation_form.html'
    success_message = "Reservation was created successfully"

    def form_valid(self, form):
        form.instance.customer_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class CancelReservationView(SuccessMessageMixin, DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
    success_message = "Reservation was cancelled successfully"

def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(customer_user=request.user)
    return render(request, 'reservation_list.html', {'reservations': reservations})

def home(request):
    return render(request, 'home.html')

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

def create_sample_menu(request):
    menu = Menu.objects.create(name="Sample Menu")
    Item.objects.create(name="Sample Item 1", price=10.00, menu=menu)
    Item.objects.create(name="Sample Item 2", price=20.00, menu=menu)
    return HttpResponseRedirect(reverse('home'))
