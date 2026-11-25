from django import forms
from .models import FoodRequest, Delivery


class FoodRequestForm(forms.ModelForm):
    class Meta:
        model = FoodRequest
        fields = ['quantity_requested', 'message']
        widgets = {
            'quantity_requested': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity required (e.g., 40)',
                'min': '0.1',
                'step': '0.1'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'e.g., Required for 50 orphaned children and seniors at our community feeding shelter in Secunderabad. We have volunteers ready to receive.'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.donation = kwargs.pop('donation', None)
        super().__init__(*args, **kwargs)

    def clean_quantity_requested(self):
        qty = self.cleaned_data.get('quantity_requested')
        if qty is None or qty <= 0:
            raise forms.ValidationError("Requested quantity must be greater than zero.")
        if self.donation and qty > self.donation.quantity:
            raise forms.ValidationError(
                f"Requested quantity cannot exceed available donation quantity of {self.donation.quantity} {self.donation.unit}."
            )
        return qty


class DeliveryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add notes on package condition, warm thermal bags, recipient trust signature (e.g., Handed over to Sister Lakshmi at ashram gate)...'
            }),
        }
