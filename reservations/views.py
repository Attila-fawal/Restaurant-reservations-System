from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Reservation, Table, Menu, Item
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import ReservationForm, UserRegisterForm, ProfileUpdateForm, CustomerProfileUpdateForm  
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.contrib.auth import login, update_session_auth_hash  
from reservations.models import Customer
from django.contrib.auth.forms import PasswordChangeForm


class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_message = "Reservation was created successfully"

    def form_valid(self, form):
        form.instance.customer_user = self.request.user
        reservation = form.save(commit=False)  # Do not save m2m fields yet
        reservation.save()  # Save the reservation instance first
        reservation.tables.set(form.cleaned_data['tables'])  # Assign the tables
        form.save_m2m()  # Save the m2m fields for ordered_items

        self.object = reservation  # Assign the object to the view
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.object is not None:  # Check if object exists
            return reverse('reservation_detail', kwargs={'pk': self.object.pk})
        else:
            # You can return a default URL if self.object doesn't exist
            return reverse('home')  


@method_decorator(login_required, name='dispatch')
class CancelReservationView(SuccessMessageMixin, DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
    success_message = "Reservation was cancelled successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CancelReservationView, self).delete(request, *args, **kwargs)


def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation_detail.html', {'reservation': reservation})


@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(customer_user=request.user).order_by('-date', '-time')
    return render(request, 'reservation_list.html', {'reservations': reservations})


def home(request):
    return render(request, 'home.html')



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
def change_password(request):  
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Customer.objects.create(user=self.object)  
        login(self.request, self.object)
        return response


def create_sample_menu(request):
    menu = Menu.objects.create(name="Sample Menu")
    Item.objects.create(name="Sample Item 1", price=10.00, menu=menu)
    Item.objects.create(name="Sample Item 2", price=20.00, menu=menu)
    return HttpResponseRedirect(reverse('home'))
