from django import forms
from .models import Vehicle, Manufacturer, CarModel, Inquiry


class VehicleForm(forms.ModelForm):
    """Form for creating and updating vehicles."""
    class Meta:
        model = Vehicle
        fields = [
            'car_model', 'vin', 'mileage', 'color', 'color_code',
            'price', 'status', 'condition', 'image', 'image_2', 'image_3',
            'description', 'features', 'is_featured'
        ]
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'mileage': forms.NumberInput(attrs={'min': '0'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'features': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sunroof, Leather Seats, Navigation, Backup Camera...'}),
            'color_code': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group car models by manufacturer for better UX
        self.fields['car_model'].queryset = CarModel.objects.select_related('manufacturer')
        self.fields['car_model'].label_from_instance = lambda obj: str(obj)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors'
            })


class ManufacturerForm(forms.ModelForm):
    """Form for creating manufacturers."""
    class Meta:
        model = Manufacturer
        fields = ['name', 'country', 'website', 'founded_year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors'
            })


class CarModelForm(forms.ModelForm):
    """Form for creating car models."""
    class Meta:
        model = CarModel
        fields = ['manufacturer', 'name', 'year', 'body_type', 'fuel_type', 'transmission', 'engine_size', 'horsepower']
        widgets = {
            'year': forms.NumberInput(attrs={'min': '1900', 'max': '2030'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors'
            })


class InquiryForm(forms.ModelForm):
    """Form for customer inquiries."""
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'I\'m interested in this vehicle. Please contact me with more details...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors'
            })


class VehicleSearchForm(forms.Form):
    """Search and filter form for vehicle listings."""
    QUERY_CHOICES = [
        ('', 'All Makes'),
    ]
    BODY_CHOICES = [('', 'All Body Types')] + CarModel.BODY_TYPE_CHOICES
    FUEL_CHOICES = [('', 'All Fuel Types')] + CarModel.FUEL_TYPE_CHOICES
    CONDITION_CHOICES = [('', 'All Conditions')] + Vehicle.Condition.choices
    SORT_CHOICES = [
        ('-added_on', 'Newest First'),
        ('added_on', 'Oldest First'),
        ('price', 'Price: Low to High'),
        ('-price', 'Price: High to Low'),
        ('-mileage', 'Highest Mileage'),
        ('mileage', 'Lowest Mileage'),
        ('-year', 'Newest Year'),
    ]

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by make, model, or keyword...',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        empty_label='All Makes',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    body_type = forms.ChoiceField(
        choices=BODY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    fuel_type = forms.ChoiceField(
        choices=FUEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    year_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Year from',
            'min': '1900',
            'max': '2030',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    year_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Year to',
            'min': '1900',
            'max': '2030',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    price_from = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min price',
            'step': '100',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    price_to = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max price',
            'step': '100',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-added_on',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
