from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Min, Max, Count

from .models import Vehicle, Manufacturer, CarModel, Inquiry
from .forms import (
    VehicleForm, ManufacturerForm, CarModelForm,
    InquiryForm, VehicleSearchForm
)


# ─── Authentication Views ─────────────────────────────────────────────

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign In'
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Account'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! You can now sign in.')
        return super().form_valid(form)


# ─── Home / Dashboard View ────────────────────────────────────────────

class HomeView(ListView):
    model = Vehicle
    template_name = 'inventory/home.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        return Vehicle.objects.filter(
            is_featured=True, status='AV'
        ).select_related('car_model__manufacturer')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Premier Auto - Drive Your Dream'
        context['manufacturers'] = Manufacturer.objects.annotate(
            vehicle_count=Count('models__vehicles')
        ).filter(vehicle_count__gt=0)[:12]
        context['total_vehicles'] = Vehicle.objects.filter(status='AV').count()
        context['total_makes'] = Manufacturer.objects.count()
        context['price_range'] = Vehicle.objects.filter(status='AV').aggregate(
            min_price=Min('price'), max_price=Max('price')
        )
        return context


# ─── Vehicle Views ────────────────────────────────────────────────────

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'inventory/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 12

    def get_queryset(self):
        queryset = Vehicle.objects.select_related(
            'car_model__manufacturer'
        ).filter(status='AV')

        form = VehicleSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            manufacturer = form.cleaned_data.get('manufacturer')
            body_type = form.cleaned_data.get('body_type')
            fuel_type = form.cleaned_data.get('fuel_type')
            condition = form.cleaned_data.get('condition')
            year_from = form.cleaned_data.get('year_from')
            year_to = form.cleaned_data.get('year_to')
            price_from = form.cleaned_data.get('price_from')
            price_to = form.cleaned_data.get('price_to')
            sort_by = form.cleaned_data.get('sort_by') or '-added_on'

            if search:
                queryset = queryset.filter(
                    Q(car_model__name__icontains=search) |
                    Q(car_model__manufacturer__name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(color__icontains=search) |
                    Q(features__icontains=search) |
                    Q(vin__icontains=search)
                )
            if manufacturer:
                queryset = queryset.filter(car_model__manufacturer=manufacturer)
            if body_type:
                queryset = queryset.filter(car_model__body_type=body_type)
            if fuel_type:
                queryset = queryset.filter(car_model__fuel_type=fuel_type)
            if condition:
                queryset = queryset.filter(condition=condition)
            if year_from:
                queryset = queryset.filter(car_model__year__gte=year_from)
            if year_to:
                queryset = queryset.filter(car_model__year__lte=year_to)
            if price_from:
                queryset = queryset.filter(price__gte=price_from)
            if price_to:
                queryset = queryset.filter(price__lte=price_to)

            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-added_on')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Browse Inventory'
        context['search_form'] = VehicleSearchForm(self.request.GET)
        context['total_results'] = self.get_queryset().count()
        return context


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'inventory/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()
        context['title'] = str(vehicle.car_model)
        context['inquiry_form'] = InquiryForm()
        context['similar_vehicles'] = Vehicle.objects.filter(
            car_model__manufacturer=vehicle.car_model.manufacturer,
            status='AV'
        ).exclude(pk=vehicle.pk).select_related('car_model__manufacturer')[:4]
        return context


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'inventory/vehicle_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Vehicle'
        context['button_text'] = 'Add Vehicle'
        return context

    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, 'Vehicle added successfully!')
        return super().form_valid(form)


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'inventory/vehicle_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Vehicle'
        context['button_text'] = 'Save Changes'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully!')
        return super().form_valid(form)


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'inventory/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Vehicle'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle deleted successfully!')
        return super().form_valid(form)


# ─── Manufacturer Views ───────────────────────────────────────────────

class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'inventory/manufacturer_list.html'
    context_object_name = 'manufacturers'

    def get_queryset(self):
        return Manufacturer.objects.annotate(
            model_count=Count('models'),
            vehicle_count=Count('models__vehicles')
        ).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Makes'
        return context


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'inventory/manufacturer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manufacturer = self.get_object()
        context['title'] = manufacturer.name
        context['vehicles'] = Vehicle.objects.filter(
            car_model__manufacturer=manufacturer,
            status='AV'
        ).select_related('car_model')[:8]
        context['models'] = CarModel.objects.filter(
            manufacturer=manufacturer
        ).annotate(vehicle_count=Count('vehicles'))
        return context


class ManufacturerCreateView(LoginRequiredMixin, CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'inventory/manufacturer_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Manufacturer'
        context['button_text'] = 'Add Manufacturer'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Manufacturer added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('manufacturer-list')


class CarModelCreateView(LoginRequiredMixin, CreateView):
    model = CarModel
    form_class = CarModelForm
    template_name = 'inventory/carmodel_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Car Model'
        context['button_text'] = 'Add Car Model'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Car model added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vehicle-create')


# ─── Inquiry View ─────────────────────────────────────────────────────

class InquiryCreateView(CreateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = 'inventory/inquiry_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact About Vehicle'
        return context

    def form_valid(self, form):
        vehicle_pk = self.kwargs.get('pk')
        vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
        form.instance.vehicle = vehicle
        messages.success(self.request, 'Your inquiry has been sent! We will get back to you soon.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vehicle-detail', kwargs={'pk': self.kwargs.get('pk')})


# ─── About View ───────────────────────────────────────────────────────

class AboutView(ListView):
    template_name = 'inventory/about.html'
    model = Vehicle

    def get(self, request, *args, **kwargs):
        from django.shortcuts import render
        return render(request, self.template_name, {
            'title': 'About Premier Auto',
            'total_vehicles': Vehicle.objects.filter(status='AV').count(),
            'total_makes': Manufacturer.objects.count(),
        })
