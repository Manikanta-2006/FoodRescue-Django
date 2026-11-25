from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_role'}),
        help_text="Select your platform role"
    )
    organization_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Grand Taj Banjara, Akshaya Seva Trust, Karachi Bakery'
        }),
        help_text="Required for NGOs, Charitable Trusts, Hotels & Catering Companies"
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Plot/Door No., Street/Road, Landmark (e.g. Near Metro Station, Banjara Hills)'
        }),
        required=True
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Hyderabad, Bengaluru, Mumbai, Delhi'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter strong password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        min_length=6
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., rahul_sharma'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name (e.g., Rahul)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name (e.g., Sharma)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address (e.g., rahul@example.in)'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email address is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')
        org_name = cleaned_data.get('organization_name')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if role == 'NGO' and not org_name:
            self.add_error('organization_name', "Trust / Organization name is mandatory for NGO accounts.")

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'organization_name', 'address', 'city', 'profile_image']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Hyderabad'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
