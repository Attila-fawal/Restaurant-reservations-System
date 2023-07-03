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
    """
    Django View for creating a Reservation. It uses LoginRequiredMixin to ensure
    the user is authenticated, and SuccessMessageMixin to show a success message
    when the reservation is successfully created.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_message = "Reservation was created successfully"

    def form_valid(self, form):
        """
        Validate the form and save a new Reservation instance.
        Also, it sets the reservation's customer_user to the current user,
        and assigns the selected tables to the reservation.
        """
        form.instance.customer_user = self.request.user
        reservation = form.save(commit=False)
        reservation.save()
        reservation.tables.set(form.cleaned_data['tables'])
        form.save_m2m()
        self.object = reservation
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Define the URL to redirect to upon successful Reservation creation.
        It redirects to the detail view of the reservation if created successfully,
        else it redirects to the home page.
        """
        if self.object is not None:
            return reverse('reservation_detail', kwargs={'pk': self.object.pk})
        else:
            return reverse('home')

@method_decorator(login_required, name='dispatch')
class CancelReservationView(SuccessMessageMixin, DeleteView):
    """
    Django View for deleting a Reservation. It uses SuccessMessageMixin to show
    a success message when the reservation is successfully cancelled.
    """
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
    success_message = "Reservation was cancelled successfully"

    def delete(self, request, *args, **kwargs):
        """
        Delete the reservation and add a success message to the request.
        """
        messages.success(self.request, self.success_message)
        return super(CancelReservationView, self).delete(request, *args, **kwargs)


def reservation_detail(request, pk):
    """
    Django View for displaying the details of a Reservation.
    It gets the Reservation instance with the provided pk (or 404 if not found),
    then renders the 'reservation_detail.html' template with the reservation instance.
    """
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

@login_required
def reservation_list(request):
    """
    Django View for displaying a list of Reservations.
    It gets all the Reservation instances of the current user, sorted by date and time,
    then renders the 'reservation_list.html' template with the reservations.
    """
    reservations = Reservation.objects.filter(customer_user=request.user).order_by('-date', '-time')
    return render(request, 'reservation_list.html', {'reservations': reservations})


def home(request):
    """
    Django View for the homepage. It simply renders the 'home.html' template.
    """
    return render(request, 'home.html')

@login_required
def update_profile(request):
    """
    Django View for updating a user's profile.
    It handles both the GET request (showing the form with the current user's data)
    and the POST request (validating and saving the submitted data).
    """
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
    """
    Django View for changing a user's password.
    It handles both the GET request (showing the form) and the POST request
    (validating and saving the new password, and updating the session hash).
    """
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
    return render(request, 'change_password.html', {'form': form})


class UserRegisterView(CreateView):
    """
    Django View for user registration.
    It creates a new User and Customer instances when the form is valid,
    and then logs in the new user.
    """
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Validate the form, save a new User instance, create a corresponding Customer instance,
        log in the new user, and then redirect to the success_url.
        """
        response = super().form_valid(form)
        Customer.objects.create(user=self.object)
        login(self.request, self.object)
        return response
