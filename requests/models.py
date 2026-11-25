from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from donations.models import Donation


class FoodRequest(models.Model):
    """
    Model representing a formal food request made by an NGO / Shelter
    for an available food donation.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending Donor Approval'),
        ('APPROVED', 'Approved by Donor'),
        ('REJECTED', 'Rejected by Donor'),
        ('CANCELLED', 'Cancelled by NGO'),
        ('COMPLETED', 'Fulfilled & Delivered'),
    ]

    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_requests')
    quantity_requested = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Quantity needed by NGO"
    )
    message = models.TextField(
        help_text="Purpose of request, number of beneficiaries, or collection notes"
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Food Request'
        verbose_name_plural = 'Food Requests'
        ordering = ['-requested_at']

    def __str__(self):
        return f"Request #{self.id} for {self.donation.food_name} by {self.receiver.username} ({self.get_status_display()})"


class Delivery(models.Model):
    """
    Model representing the transportation and logistics of approved food donations
    from the donor's address to the receiver's premises by a volunteer.
    """
    DELIVERY_STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned / Waiting for Volunteer Pickup'),
        ('PICKED_UP', 'Food Collected from Donor'),
        ('IN_TRANSIT', 'In Transit to Receiver'),
        ('DELIVERED', 'Delivered to Receiver'),
        ('CANCELLED', 'Delivery Cancelled'),
    ]

    food_request = models.OneToOneField(FoodRequest, on_delete=models.CASCADE, related_name='delivery')
    volunteer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries',
        help_text="Volunteer assigned to collect and deliver"
    )
    pickup_time = models.DateTimeField(null=True, blank=True, help_text="Time food was picked up")
    delivery_time = models.DateTimeField(null=True, blank=True, help_text="Time food was handed over")
    delivery_status = models.CharField(
        max_length=30,
        choices=DELIVERY_STATUS_CHOICES,
        default='ASSIGNED'
    )
    remarks = models.TextField(
        blank=True,
        default='',
        help_text="Notes on food temperature, packing condition, handover details"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Delivery Task'
        verbose_name_plural = 'Delivery Tasks'
        ordering = ['-created_at']

    def __str__(self):
        vol_name = self.volunteer.get_full_name() or self.volunteer.username if self.volunteer else "Unassigned"
        return f"Delivery #{self.id} [{self.get_delivery_status_display()}] - Vol: {vol_name}"

    def mark_picked_up(self, volunteer_user=None):
        if volunteer_user and not self.volunteer:
            self.volunteer = volunteer_user
        self.delivery_status = 'PICKED_UP'
        self.pickup_time = timezone.now()
        self.save()

        # Update donation status as well
        donation = self.food_request.donation
        donation.status = 'COLLECTED'
        donation.save()

    def mark_delivered(self, remarks=None):
        self.delivery_status = 'DELIVERED'
        self.delivery_time = timezone.now()
        if remarks:
            self.remarks = remarks
        self.save()

        # Update food request & donation status
        self.food_request.status = 'COMPLETED'
        self.food_request.save()

        donation = self.food_request.donation
        donation.status = 'DELIVERED'
        donation.save()
