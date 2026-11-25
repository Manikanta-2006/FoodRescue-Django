import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Donation(models.Model):
    """
    Model representing surplus Indian food donated by hotels, wedding halls,
    caterers, corporate canteens, restaurants, or individuals.
    """
    CATEGORY_CHOICES = [
        ('COOKED_MEALS', 'Cooked Meals (Biryani, Pulao, Curries, Rotis, Thali)'),
        ('RAW_GROCERIES', 'Raw Groceries & Pulses (Atta, Rice, Dal, Spices)'),
        ('BAKERY_BREAD', 'Bakery, Pav, Roti & Naan'),
        ('FRUITS_VEGGIES', 'Fresh Mandi Fruits & Vegetables'),
        ('DAIRY', 'Dairy & Milk (Amul Milk, Paneer, Curd, Ghee)'),
        ('PACKED_FOOD', 'Packaged & Dry Snacks (Namkeen, Biscuits, Poha)'),
        ('SWEETS_MITHAI', 'Indian Sweets & Mithai (Gulab Jamun, Ladoo, Halwa)'),
        ('OTHER', 'Other Indian Food Items'),
    ]

    UNIT_CHOICES = [
        ('plates', 'Plates / Thalis'),
        ('kg', 'Kilograms (kg)'),
        ('packets', 'Packets / Boxes'),
        ('liters', 'Liters (L)'),
        ('servings', 'Servings (Persons)'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available for Request'),
        ('REQUESTED', 'Request Pending'),
        ('ACCEPTED', 'Accepted (Awaiting Volunteer Pickup)'),
        ('COLLECTED', 'Collected (In Transit)'),
        ('DELIVERED', 'Delivered to Shelter / NGO'),
        ('EXPIRED', 'Expired / Spoiled'),
        ('CANCELLED', 'Cancelled by Donor'),
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    food_name = models.CharField(max_length=150, help_text="e.g., Hyderabadi Veg Dum Biryani, 50 Paneer Butter Masala Packets")
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="URL friendly slug")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='COOKED_MEALS')
    description = models.TextField(help_text="Details about spices, Veg/Non-veg tag, packing condition, heating tips...")
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text="Total portion/weight count")
    unit = models.CharField(max_length=30, choices=UNIT_CHOICES, default='plates')
    prepared_at = models.DateTimeField(help_text="Date and time when food was cooked or packed")
    expiry_at = models.DateTimeField(help_text="Best before / safe consumption deadline")
    pickup_address = models.TextField(help_text="Detailed address (e.g. Banquet Kitchen, Road No. 12, Banjara Hills)")
    city = models.CharField(max_length=100, default='Hyderabad', help_text="City (e.g. Hyderabad, Bengaluru, Mumbai, Delhi)")
    food_image = models.ImageField(upload_to='donations/', blank=True, null=True, help_text="Photo of the food containers")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Food Donation'
        verbose_name_plural = 'Food Donations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.food_name} ({self.quantity} {self.unit}) - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.food_name) or 'indian-food-donation'
            unique_slug = base_slug
            while Donation.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug
        
        # Check if expired automatically
        if self.expiry_at and timezone.now() > self.expiry_at and self.status == 'AVAILABLE':
            self.status = 'EXPIRED'

        super().save(*args, **kwargs)

    def is_expired(self):
        if self.expiry_at:
            return timezone.now() > self.expiry_at
        return False

    @property
    def is_active(self):
        return self.status == 'AVAILABLE' and not self.is_expired()

    @property
    def get_image_url(self):
        """
        Returns uploaded food image URL, or a curated high-resolution photo
        matching the specific Indian food item or category.
        """
        if self.food_image:
            try:
                return self.food_image.url
            except Exception:
                pass

        # Specific matches by Indian dish name keywords
        name_lower = self.food_name.lower()
        if 'biryani' in name_lower:
            return 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80'
        elif 'thali' in name_lower or 'makhani' in name_lower or 'sabzi' in name_lower:
            return 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80'
        elif 'pav' in name_lower or 'biscuit' in name_lower or 'rusk' in name_lower:
            return 'https://images.unsplash.com/photo-1608198093002-ad4e005484ec?auto=format&fit=crop&w=800&q=80'
        elif 'idli' in name_lower or 'vada' in name_lower or 'dosa' in name_lower or 'tiffin' in name_lower:
            return 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80'
        elif 'mango' in name_lower or 'orange' in name_lower or 'fruit' in name_lower:
            return 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&w=800&q=80'
        elif 'milk' in name_lower or 'paneer' in name_lower or 'curd' in name_lower:
            return 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80'
        elif 'atta' in name_lower or 'dal' in name_lower or 'rice' in name_lower:
            return 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80'
        elif 'pulao' in name_lower or 'box' in name_lower:
            return 'https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?auto=format&fit=crop&w=800&q=80'
        elif 'mithai' in name_lower or 'ladoo' in name_lower or 'sweet' in name_lower or 'halwa' in name_lower:
            return 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80'

        # Category fallbacks
        category_photos = {
            'COOKED_MEALS': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80',
            'RAW_GROCERIES': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
            'BAKERY_BREAD': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80',
            'FRUITS_VEGGIES': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&w=800&q=80',
            'DAIRY': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da?auto=format&fit=crop&w=800&q=80',
            'PACKED_FOOD': 'https://images.unsplash.com/photo-1621996346565-e3d5d6281292?auto=format&fit=crop&w=800&q=80',
            'SWEETS_MITHAI': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80',
            'OTHER': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80',
        }
        return category_photos.get(self.category, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80')

    def get_absolute_url(self):
        return reverse('donations:donation_detail_slug', kwargs={'slug': self.slug})
