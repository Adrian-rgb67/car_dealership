from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # Vehicle CRUD
    path('inventory/', views.VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/add/', views.VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicle/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicle/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle-delete'),

    # Vehicle Inquiry
    path('vehicle/<int:pk>/inquiry/', views.InquiryCreateView.as_view(), name='vehicle-inquiry'),

    # Manufacturers
    path('makes/', views.ManufacturerListView.as_view(), name='manufacturer-list'),
    path('makes/<int:pk>/', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
    path('makes/add/', views.ManufacturerCreateView.as_view(), name='manufacturer-create'),

    # Car Model
    path('model/add/', views.CarModelCreateView.as_view(), name='carmodel-create'),

    # About
    path('about/', views.AboutView.as_view(), name='about'),
]
