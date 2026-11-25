from django import forms
from django.utils import timezone
from .models import Donation


class DonationForm(forms.ModelForm):
    prepared_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        help_text="When was this food cooked or prepared in the kitchen?"
    )
    expiry_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        help_text="Best before / safe consumption time (IST)"
    )

    class Meta:
        model = Donation
        fields = [
            'food_name',
            'category',
            'quantity',
            'unit',
            'prepared_at',
            'expiry_at',
            'pickup_address',
            'city',
            'food_image',
            'description',
        ]
        widgets = {
            'food_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 60 Plates of Hyderabadi Dum Biryani with Raita'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 50',
                'min': '0.1',
                'step': '0.1'
            }),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'pickup_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Banquet Hall Kitchen, Road No. 12, Banjara Hills, Near Metro Pillar 1045'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Hyderabad, Bengaluru, Mumbai, Delhi NCR, Chennai, Pune'
            }),
            'food_image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Specify dietary details (100% Veg / Non-Veg, Jain-friendly, No onion/garlic), packaging containers (aluminum foil, food-grade boxes), and temperature conditions...'
            }),
        }

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise forms.ValidationError("Quantity must be a positive number greater than 0.")
        return qty

    def clean(self):
        cleaned_data = super().clean()
        prep = cleaned_data.get('prepared_at')
        exp = cleaned_data.get('expiry_at')

        if prep and exp:
            if exp <= prep:
                self.add_error('expiry_at', "Expiry time must be later than preparation time.")
            if exp <= timezone.now():
                self.add_error('expiry_at', "Expiry date and time cannot be in the past.")

        return cleaned_data
