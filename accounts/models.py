from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extends standard Django User model to store role, contact,
    organization info, and verification status for Indian NGOs & Donors.
    """
    ROLE_CHOICES = [
        ('Donor', 'Food Donor (Restaurant / Hotel / Banquet / Caterer)'),
        ('NGO', 'NGO / Trust / Shelter / Orphanage Receiver'),
        ('Volunteer', 'Food Rescue Volunteer (Courier / Transporter)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Donor')
    phone = models.CharField(max_length=20, blank=True, help_text="e.g., +91 98765 43210")
    organization_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name of Restaurant, Hotel, NGO Trust, or Catering Hall"
    )
    address = models.TextField(blank=True, help_text="Plot/Flat, Street, Locality (e.g. Jubilee Hills, Road No. 10)")
    city = models.CharField(max_length=100, blank=True, default='Hyderabad')
    is_verified = models.BooleanField(
        default=False,
        help_text="Government / NGO Darpan verification status"
    )
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        org = f" ({self.organization_name})" if self.organization_name else ""
        return f"{self.user.get_full_name() or self.user.username} [{self.role}]{org}"

    @property
    def is_donor(self):
        return self.role == 'Donor'

    @property
    def is_ngo(self):
        return self.role == 'NGO'

    @property
    def is_volunteer(self):
        return self.role == 'Volunteer'


# Signal to create user profile automatically upon user registration
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
