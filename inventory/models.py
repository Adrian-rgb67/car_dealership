from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Manufacturer(models.Model):
    """Represents a car manufacturer (e.g., Ford, Toyota)."""
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='manufacturer_logos/', blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturer-detail', kwargs={'pk': self.pk})


class CarModel(models.Model):
    """Represents a specific model from a manufacturer (e.g., Mustang)."""
    BODY_TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('WAGON', 'Wagon'),
    ]
    FUEL_TYPE_CHOICES = [
        ('GASOLINE', 'Gasoline'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
        ('PLUGIN_HYBRID', 'Plug-in Hybrid'),
    ]
    TRANSMISSION_CHOICES = [
        ('AUTOMATIC', 'Automatic'),
        ('MANUAL', 'Manual'),
        ('CVT', 'CVT'),
        ('DUAL_CLUTCH', 'Dual-Clutch'),
    ]

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, blank=True)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, blank=True)
    engine_size = models.CharField(max_length=50, blank=True, help_text="e.g., 3.5L V6")
    horsepower = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ['manufacturer', 'name', 'year']
        ordering = ['manufacturer', 'name', '-year']

    def __str__(self):
        return f"{self.manufacturer.name} {self.name} ({self.year})"


class Vehicle(models.Model):
    """Represents a physical vehicle for sale on the lot."""

    class Status(models.TextChoices):
        AVAILABLE = 'AV', 'Available'
        PENDING = 'PE', 'Sale Pending'
        SOLD = 'SO', 'Sold'

    class Condition(models.TextChoices):
        NEW = 'NEW', 'Brand New'
        LIKE_NEW = 'LN', 'Like New'
        EXCELLENT = 'EX', 'Excellent'
        GOOD = 'GD', 'Good'
        FAIR = 'FR', 'Fair'

    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='vehicles')
    vin = models.CharField('VIN', max_length=17, unique=True)
    mileage = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, blank=True, help_text="Hex color code, e.g., #FF0000")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.AVAILABLE)
    condition = models.CharField(max_length=3, choices=Condition.choices, default=Condition.EXCELLENT)
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="Comma-separated features, e.g., Sunroof, Leather Seats, NAV")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Featured vehicles appear on the homepage")

    class Meta:
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.car_model} - {self.vin}"

    def get_absolute_url(self):
        return reverse('vehicle-detail', kwargs={'pk': self.pk})

    @property
    def formatted_price(self):
        return f"${self.price:,.2f}"

    @property
    def formatted_mileage(self):
        return f"{self.mileage:,}"

    @property
    def features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',') if f.strip()]
        return []

    @property
    def status_badge_class(self):
        badges = {
            'AV': 'bg-emerald-100 text-emerald-800',
            'PE': 'bg-amber-100 text-amber-800',
            'SO': 'bg-red-100 text-red-800',
        }
        return badges.get(self.status, 'bg-gray-100 text-gray-800')


class Inquiry(models.Model):
    """Customer inquiries about vehicles."""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry from {self.name} about {self.vehicle}"
