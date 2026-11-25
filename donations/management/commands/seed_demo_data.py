from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import UserProfile
from donations.models import Donation
from requests.models import FoodRequest, Delivery


class Command(BaseCommand):
    help = 'Seeds database with realistic Indian demo accounts, authentic Indian food donations, NGO requests, and volunteer deliveries.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting Indian database demo data seeding..."))

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@foodrescue.in',
                'first_name': 'Kalyan',
                'last_name': 'Chakravarthy',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        admin_prof, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_prof.role = 'Donor'
        admin_prof.phone = '+91 98480 12345'
        admin_prof.organization_name = 'FoodRescue India Central Directorate'
        admin_prof.address = 'Hitec City, Madhapur, Hyderabad'
        admin_prof.city = 'Hyderabad'
        admin_prof.is_verified = True
        admin_prof.save()

        # 2. Donor 1: Taj Banjara Hotel, Hyderabad
        taj_user, created = User.objects.get_or_create(
            username='taj_hotel',
            defaults={
                'email': 'banquets@tajbanjara.com',
                'first_name': 'Rajesh',
                'last_name': 'Varma',
            }
        )
        taj_user.set_password('donor123')
        taj_user.save()
        taj_prof, _ = UserProfile.objects.get_or_create(user=taj_user)
        taj_prof.role = 'Donor'
        taj_prof.organization_name = 'Grand Taj Banjara Hotel & Banquets'
        taj_prof.phone = '+91 98490 12345'
        taj_prof.address = 'Road No. 1, Banjara Hills, Hyderabad, Telangana'
        taj_prof.city = 'Hyderabad'
        taj_prof.is_verified = True
        taj_prof.save()

        # 3. Donor 2: Karachi Bakery & Sweets, Hyderabad
        karachi_user, created = User.objects.get_or_create(
            username='city_bakery',
            defaults={
                'email': 'orders@karachibakery.in',
                'first_name': 'Harish',
                'last_name': 'Ramani',
            }
        )
        karachi_user.set_password('donor123')
        karachi_user.save()
        karachi_prof, _ = UserProfile.objects.get_or_create(user=karachi_user)
        karachi_prof.role = 'Donor'
        karachi_prof.organization_name = 'Karachi Bakery & Sweets'
        karachi_prof.phone = '+91 98850 67890'
        karachi_prof.address = 'Mozamjahi Market, Abids, Hyderabad, Telangana'
        karachi_prof.city = 'Hyderabad'
        karachi_prof.is_verified = True
        karachi_prof.save()

        # 4. Donor 3: Annapurna Wedding Caterers, Bengaluru
        annapurna_user, created = User.objects.get_or_create(
            username='annapurna_caterers',
            defaults={
                'email': 'contact@annapurnacaterers.in',
                'first_name': 'Senthil',
                'last_name': 'Kumar',
            }
        )
        annapurna_user.set_password('donor123')
        annapurna_user.save()
        annapurna_prof, _ = UserProfile.objects.get_or_create(user=annapurna_user)
        annapurna_prof.role = 'Donor'
        annapurna_prof.organization_name = 'Annapurna Grand Wedding Caterers'
        annapurna_prof.phone = '+91 94440 23456'
        annapurna_prof.address = '100 Feet Road, Indiranagar, Bengaluru, Karnataka'
        annapurna_prof.city = 'Bengaluru'
        annapurna_prof.is_verified = True
        annapurna_prof.save()

        # 5. NGO 1: Akshaya Seva Foundation, Hyderabad
        akshaya_user, created = User.objects.get_or_create(
            username='hope_shelter',
            defaults={
                'email': 'seva@akshayafoundation.org.in',
                'first_name': 'Venkat',
                'last_name': 'Rao',
            }
        )
        akshaya_user.set_password('ngo12345')
        akshaya_user.save()
        akshaya_prof, _ = UserProfile.objects.get_or_create(user=akshaya_user)
        akshaya_prof.role = 'NGO'
        akshaya_prof.organization_name = 'Akshaya Seva Community Kitchen & Shelter'
        akshaya_prof.phone = '+91 98765 43210'
        akshaya_prof.address = 'Near Clock Tower, Secunderabad, Hyderabad, Telangana'
        akshaya_prof.city = 'Hyderabad'
        akshaya_prof.is_verified = True
        akshaya_prof.save()

        # 6. NGO 2: Sneha Child Welfare Home, Hyderabad
        sneha_user, created = User.objects.get_or_create(
            username='sunshine_home',
            defaults={
                'email': 'care@snehahome.org.in',
                'first_name': 'Sunita',
                'last_name': 'Reddy',
            }
        )
        sneha_user.set_password('ngo12345')
        sneha_user.save()
        sneha_prof, _ = UserProfile.objects.get_or_create(user=sneha_user)
        sneha_prof.role = 'NGO'
        sneha_prof.organization_name = 'Sneha Destitute Children Care Home'
        sneha_prof.phone = '+91 99887 76655'
        sneha_prof.address = 'Plot 18, Road No. 36, Jubilee Hills, Hyderabad, Telangana'
        sneha_prof.city = 'Hyderabad'
        sneha_prof.is_verified = True
        sneha_prof.save()

        # 7. Volunteer 1: Ramesh Kumar, Hyderabad
        ramesh_user, created = User.objects.get_or_create(
            username='alex_courier',
            defaults={
                'email': 'ramesh@volunteerindia.org',
                'first_name': 'Ramesh',
                'last_name': 'Kumar',
            }
        )
        ramesh_user.set_password('vol12345')
        ramesh_user.save()
        ramesh_prof, _ = UserProfile.objects.get_or_create(user=ramesh_user)
        ramesh_prof.role = 'Volunteer'
        ramesh_prof.phone = '+91 91234 56789'
        ramesh_prof.address = 'Ameerpet Metro Station Hub, Hyderabad'
        ramesh_prof.city = 'Hyderabad'
        ramesh_prof.is_verified = True
        ramesh_prof.save()

        # 8. Volunteer 2: Priya Sharma, Bengaluru
        priya_user, created = User.objects.get_or_create(
            username='priya_express',
            defaults={
                'email': 'priya.sharma@rescuebengaluru.org',
                'first_name': 'Priya',
                'last_name': 'Sharma',
            }
        )
        priya_user.set_password('vol12345')
        priya_user.save()
        priya_prof, _ = UserProfile.objects.get_or_create(user=priya_user)
        priya_prof.role = 'Volunteer'
        priya_prof.phone = '+91 80081 23456'
        priya_prof.address = 'Koramangala 4th Block, Bengaluru, Karnataka'
        priya_prof.city = 'Bengaluru'
        priya_prof.is_verified = True
        priya_prof.save()

        self.stdout.write(self.style.SUCCESS("Indian User accounts created / updated."))

        # Delete existing sample donations to ensure pure Indian dataset
        Donation.objects.all().delete()

        now = timezone.now()

        indian_donations = [
            {
                'donor': taj_user,
                'food_name': 'Hyderabadi Veg Dum Biryani with Mirchi Ka Salan',
                'category': 'COOKED_MEALS',
                'quantity': 70.0,
                'unit': 'plates',
                'description': 'Authentic slow-cooked dum biryani prepared with premium aged Daawat basmati rice, farm fresh vegetables, paneer cubes, saffron, and aromatic Indian spices. Includes sealed bowls of Mirchi Ka Salan and onion-mint raita. Cooked for a corporate luncheon and stored in insulated food containers at 65°C.',
                'prepared_at': now - timedelta(hours=2),
                'expiry_at': now + timedelta(hours=9),
                'pickup_address': 'Road No. 1, Banjara Hills, Grand Taj Banquet Kitchen Gate 4',
                'city': 'Hyderabad',
                'status': 'AVAILABLE'
            },
            {
                'donor': karachi_user,
                'food_name': 'Fresh Pav Buns, Rusk & Osmania Biscuits',
                'category': 'BAKERY_BREAD',
                'quantity': 50.0,
                'unit': 'packets',
                'description': 'Soft fresh Mumbai pav buns, crunchy butter rusks, and world-famous Hyderabad Osmania biscuits baked fresh this morning. Packed in food-grade sealed cartons.',
                'prepared_at': now - timedelta(hours=4),
                'expiry_at': now + timedelta(hours=36),
                'pickup_address': 'Mozamjahi Market, Abids, Loading Dock',
                'city': 'Hyderabad',
                'status': 'AVAILABLE'
            },
            {
                'donor': annapurna_user,
                'food_name': 'South Indian Tiffin (Idli, Medu Vada & Sambar)',
                'category': 'COOKED_MEALS',
                'quantity': 90.0,
                'unit': 'plates',
                'description': 'Steaming hot soft rice idlis and crispy medu vadas with piping hot Madras vegetable sambar and fresh grated coconut chutney. Prepared for a wedding breakfast reception.',
                'prepared_at': now - timedelta(hours=3),
                'expiry_at': now + timedelta(hours=8),
                'pickup_address': 'Annapurna Convention Hall, 100 Feet Road, Indiranagar',
                'city': 'Bengaluru',
                'status': 'AVAILABLE'
            },
            {
                'donor': taj_user,
                'food_name': 'Fresh Alphonso Mangoes & Nagpur Oranges',
                'category': 'FRUITS_VEGGIES',
                'quantity': 85.0,
                'unit': 'kg',
                'description': 'Grade-A fresh Mandi fruits from breakfast buffet supply. Sweet Ratnagiri Alphonso mangoes, juicy Nagpur oranges, and Robusta bananas. Cleaned and crated.',
                'prepared_at': now - timedelta(hours=5),
                'expiry_at': now + timedelta(days=3),
                'pickup_address': 'Cold Storage Bay 2, Taj Banjara, Road No. 1, Banjara Hills',
                'city': 'Hyderabad',
                'status': 'AVAILABLE'
            },
            {
                'donor': annapurna_user,
                'food_name': 'Amul Taaza Milk Pouches & Fresh Malai Paneer',
                'category': 'DAIRY',
                'quantity': 45.0,
                'unit': 'liters',
                'description': 'Unopened 500ml pasteurized Amul Taaza milk pouches and 10 kg of vacuum-packed fresh malai paneer kept under 4°C deep refrigeration.',
                'prepared_at': now - timedelta(hours=6),
                'expiry_at': now + timedelta(hours=20),
                'pickup_address': 'Refrigeration Unit, Annapurna Hall, Indiranagar',
                'city': 'Bengaluru',
                'status': 'REQUESTED'
            },
            {
                'donor': taj_user,
                'food_name': 'North Indian Thali (Dal Makhani, Paneer & Rotis)',
                'category': 'COOKED_MEALS',
                'quantity': 60.0,
                'unit': 'plates',
                'description': 'Rich slow-cooked Dal Makhani, Paneer Butter Masala, soft butter rotis, and jeera rice. Complete dinner portions packed in 5-compartment meal trays.',
                'prepared_at': now - timedelta(hours=3),
                'expiry_at': now + timedelta(hours=7),
                'pickup_address': 'Banjara Banquet Gate 3, Road No. 1, Banjara Hills',
                'city': 'Hyderabad',
                'status': 'ACCEPTED'
            },
            {
                'donor': taj_user,
                'food_name': 'Aashirvaad Sharbati Atta & Tata Sampann Toor Dal',
                'category': 'RAW_GROCERIES',
                'quantity': 40.0,
                'unit': 'kg',
                'description': 'Sealed 10 kg bags of Aashirvaad Sharbati Whole Wheat Atta and 1 kg pouches of unpolished Toor Dal and Moong Dal.',
                'prepared_at': now - timedelta(days=1),
                'expiry_at': now + timedelta(days=90),
                'pickup_address': 'Pantry Warehouse, Taj Banjara, Banjara Hills',
                'city': 'Hyderabad',
                'status': 'COLLECTED'
            },
            {
                'donor': taj_user,
                'food_name': '100 Vegetable Pulao Meal Boxes with Gulab Jamun',
                'category': 'COOKED_MEALS',
                'quantity': 100.0,
                'unit': 'plates',
                'description': 'Nutritious fragrant vegetable pulao, boondi raita, and sweet hot Gulab Jamuns. Successfully collected and distributed to children at Sneha Care Home.',
                'prepared_at': now - timedelta(days=1, hours=5),
                'expiry_at': now - timedelta(hours=2),
                'pickup_address': 'Grand Taj Banjara Service Kitchen',
                'city': 'Hyderabad',
                'status': 'DELIVERED'
            },
            {
                'donor': karachi_user,
                'food_name': 'Royal Indian Mithai Assortment (Ladoo & Halwa)',
                'category': 'SWEETS_MITHAI',
                'quantity': 30.0,
                'unit': 'kg',
                'description': 'Pure Desi Ghee Motichoor Ladoos, Moong Dal Halwa, and Kaju Katli boxes from festival catering.',
                'prepared_at': now - timedelta(days=1, hours=8),
                'expiry_at': now + timedelta(days=5),
                'pickup_address': 'Karachi Bakery, Abids Main Counter',
                'city': 'Hyderabad',
                'status': 'DELIVERED'
            }
        ]

        created_donations = []
        for d in indian_donations:
            donation_obj = Donation.objects.create(**d)
            created_donations.append(donation_obj)

        self.stdout.write(self.style.SUCCESS(f"{len(created_donations)} authentic Indian food donations seeded."))

        # 9. Create Linked Requests and Deliveries
        # A. Pending Request: Item 4 (Amul Milk & Paneer)
        d_milk = created_donations[4]
        FoodRequest.objects.create(
            donation=d_milk,
            receiver=sneha_user,
            quantity_requested=35.0,
            message="Urgent nutrition requirement for 45 growing children and toddlers at Sneha Care Home in Jubilee Hills. We have milk heating equipment ready.",
            status='PENDING'
        )

        # B. Approved Request & Delivery ASSIGNED: Item 5 (North Indian Thali)
        d_thali = created_donations[5]
        req_thali = FoodRequest.objects.create(
            donation=d_thali,
            receiver=akshaya_user,
            quantity_requested=60.0,
            message="Required for our evening night-shelter langar / distribution near Secunderabad Station.",
            status='APPROVED'
        )
        Delivery.objects.create(
            food_request=req_thali,
            delivery_status='ASSIGNED',
            volunteer=None,
            remarks="Waiting for volunteer courier to claim pickup from Banjara Hills to Secunderabad."
        )

        # C. COLLECTED (In Transit): Item 6 (Atta & Toor Dal)
        d_groceries = created_donations[6]
        req_groceries = FoodRequest.objects.create(
            donation=d_groceries,
            receiver=akshaya_user,
            quantity_requested=40.0,
            message="Raw pulses and flour for our community free kitchen pantry.",
            status='APPROVED'
        )
        Delivery.objects.create(
            food_request=req_groceries,
            volunteer=ramesh_user,
            pickup_time=now - timedelta(minutes=35),
            delivery_status='PICKED_UP',
            remarks="[Pickup at Banjara Hills]: Inspected 4 bags of 10kg Atta and 10 pouches of Tata Sampann Toor Dal. All sealed tight. Loaded onto delivery two-wheeler carrier."
        )

        # D. DELIVERED: Item 7 (100 Veg Pulao & Gulab Jamun)
        d_pulao = created_donations[7]
        req_pulao = FoodRequest.objects.create(
            donation=d_pulao,
            receiver=sneha_user,
            quantity_requested=100.0,
            message="Dinner drive for 80 children and 20 resident caregivers at Jubilee Hills center.",
            status='COMPLETED'
        )
        Delivery.objects.create(
            food_request=req_pulao,
            volunteer=ramesh_user,
            pickup_time=now - timedelta(days=1, hours=4),
            delivery_time=now - timedelta(days=1, hours=2, minutes=15),
            delivery_status='DELIVERED',
            remarks="Handed over 100 hot meal boxes and dessert containers to Incharge Sister Sunita Reddy at Jubilee Hills gate. Food hot and fresh. Signed handover token #AK-402."
        )

        # E. DELIVERED: Item 8 (Indian Mithai)
        d_mithai = created_donations[8]
        req_mithai = FoodRequest.objects.create(
            donation=d_mithai,
            receiver=akshaya_user,
            quantity_requested=30.0,
            message="Festival sweet distribution for destitute seniors and street children.",
            status='COMPLETED'
        )
        Delivery.objects.create(
            food_request=req_mithai,
            volunteer=priya_user,
            pickup_time=now - timedelta(days=1, hours=6),
            delivery_time=now - timedelta(days=1, hours=4),
            delivery_status='DELIVERED',
            remarks="30 kg pure desi ghee mithai delivered to Venkat Rao at Secunderabad ashram. 100% verified."
        )

        self.stdout.write(self.style.SUCCESS("All Indian requests and deliveries created successfully!"))
        self.stdout.write(self.style.SUCCESS("\n=========================================="))
        self.stdout.write(self.style.SUCCESS("INDIAN DEMO ACCOUNTS & CREDENTIALS"))
        self.stdout.write(self.style.SUCCESS("=========================================="))
        self.stdout.write("  Admin:       admin / admin123        (Kalyan Chakravarthy - Hyderabad)")
        self.stdout.write("  Donor 1:     taj_hotel / donor123    (Grand Taj Banjara - Hyderabad)")
        self.stdout.write("  Donor 2:     city_bakery / donor123  (Karachi Bakery & Sweets - Hyderabad)")
        self.stdout.write("  Donor 3:     annapurna_caterers / donor123 (Annapurna Caterers - Bengaluru)")
        self.stdout.write("  NGO 1:       hope_shelter / ngo12345 (Akshaya Seva Foundation - Hyderabad)")
        self.stdout.write("  NGO 2:       sunshine_home / ngo12345 (Sneha Children Home - Jubilee Hills)")
        self.stdout.write("  Volunteer 1: alex_courier / vol12345 (Ramesh Kumar - Hyderabad Courier)")
        self.stdout.write("  Volunteer 2: priya_express / vol12345 (Priya Sharma - Bengaluru Courier)")
        self.stdout.write(self.style.SUCCESS("=========================================="))
