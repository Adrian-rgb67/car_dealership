from django.contrib import admin
from .models import Manufacturer, CarModel, Vehicle, Inquiry


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year']
    search_fields = ['name', 'country']
    prepopulated_fields = {}


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'year', 'body_type', 'fuel_type']
    list_filter = ['manufacturer', 'body_type', 'fuel_type', 'transmission']
    search_fields = ['name', 'manufacturer__name']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'vin', 'price', 'mileage', 'status', 'condition', 'added_on']
    list_filter = ['status', 'condition', 'car_model__manufacturer', 'car_model__body_type']
    search_fields = ['vin', 'car_model__name', 'car_model__manufacturer__name']
    list_editable = ['status', 'price']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'vehicle', 'created_on', 'is_read']
    list_filter = ['is_read', 'created_on']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'message']
