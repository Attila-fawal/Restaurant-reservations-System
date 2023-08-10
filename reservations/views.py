from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Reservation, Table, Menu, Item
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import ReservationForm, UserRegisterForm, ProfileUpdateForm, CustomerProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.contrib.auth import login, update_session_auth_hash
from .models import Customer
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView


User = get_user_model()


class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_message = "Reservation was created successfully"

    def form_valid(self, form):
        form.instance.customer_user = self.request.user
        reservation = form.save(commit=False)
        reservation.save()

        # Ensure 'tables' key exists in cleaned_data before accessing
        if 'tables' in form.cleaned_data:
            reservation.tables.set(form.cleaned_data['tables'])
        form.save_m2m()

        self.object = reservation
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.object is not None:
            return reverse('reservation_detail', kwargs={'pk': self.object.pk})
        else:
            return reverse('home')


@method_decorator(login_required, name='dispatch')
class CancelReservationView(SuccessMessageMixin, DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
    success_message = "Reservation was cancelled successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CancelReservationView, self)\
            .delete(request, *args, **kwargs)


def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation_detail.html',
                  {'reservation': reservation})


@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(
        customer_user=request.user).order_by('-date', '-time')
    return render(request, 'reservation_list.html',
                  {'reservations': reservations})


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
            messages.success(
                request,
                'Your password was successfully updated!'
            )
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def delete_account(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    messages.success(request, 'Your account has been deleted.')
    return redirect('home')


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Customer.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class DeleteAccountView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'delete_account.html'
    success_url = reverse_lazy('home')
    success_message = "Your account has been deleted successfully"

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'

    def get_initial(self):
        initial = super().get_initial()
        reservation = self.get_object()
        initial['date'] = ""
        initial['time'] = ""
        return initial

    def form_valid(self, form):
        form.instance.customer_user = self.request.user
        reservation = form.save(commit=False)
        reservation.save()

        # Ensure 'tables' key exists in cleaned_data before accessing
        if 'tables' in form.cleaned_data:
            reservation.tables.set(form.cleaned_data['tables'])
        form.save_m2m()

        self.object = reservation
        messages.success(self.request, "Reservation successfully updated!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.object.pk})

