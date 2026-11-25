from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from accounts.models import UserProfile
from donations.models import Donation
from requests.models import FoodRequest, Delivery


class FoodRescuePlatformTests(TestCase):
    """
    Automated test suite fulfilling INT253 Academic Requirements:
    1. Endpoint testing & authentication
    2. Donation creation & slug generation
    3. Database-driven search & filtering
    4. Invalid record handling (404 error)
    5. JSON API endpoint responses
    6. Complete Food Request & Delivery lifecycle
    7. Role dashboard authorization access
    """

    def setUp(self):
        self.client = Client()

        # 1. Create Indian Donor User
        self.donor_user = User.objects.create_user(
            username='chef_rajesh',
            email='rajesh@tajbanjara.com',
            password='password123',
            first_name='Rajesh',
            last_name='Varma'
        )
        self.donor_profile = self.donor_user.profile
        self.donor_profile.role = 'Donor'
        self.donor_profile.organization_name = 'Grand Taj Banjara Banquets'
        self.donor_profile.phone = '+91 98490 12345'
        self.donor_profile.address = 'Road No. 1, Banjara Hills'
        self.donor_profile.city = 'Hyderabad'
        self.donor_profile.is_verified = True
        self.donor_profile.save()

        # 2. Create Indian NGO User
        self.ngo_user = User.objects.create_user(
            username='sister_sunita',
            email='sunita@snehahome.org.in',
            password='password123',
            first_name='Sunita',
            last_name='Reddy'
        )
        self.ngo_profile = self.ngo_user.profile
        self.ngo_profile.role = 'NGO'
        self.ngo_profile.organization_name = 'Sneha Children Welfare Home'
        self.ngo_profile.phone = '+91 99887 76655'
        self.ngo_profile.address = 'Plot 18, Road No. 36, Jubilee Hills'
        self.ngo_profile.city = 'Hyderabad'
        self.ngo_profile.is_verified = True
        self.ngo_profile.save()

        # 3. Create Indian Volunteer User
        self.vol_user = User.objects.create_user(
            username='ramesh_courier',
            email='ramesh@volunteerindia.org',
            password='password123',
            first_name='Ramesh',
            last_name='Kumar'
        )
        self.vol_profile = self.vol_user.profile
        self.vol_profile.role = 'Volunteer'
        self.vol_profile.phone = '+91 91234 56789'
        self.vol_profile.address = 'Ameerpet Metro Hub'
        self.vol_profile.city = 'Hyderabad'
        self.vol_profile.is_verified = True
        self.vol_profile.save()

        # 4. Create an initial active Indian donation
        now = timezone.now()
        self.donation = Donation.objects.create(
            donor=self.donor_user,
            food_name='Hyderabadi Veg Dum Biryani',
            category='COOKED_MEALS',
            description='Authentic slow-cooked saffron dum biryani from wedding banquet.',
            quantity=50.0,
            unit='plates',
            prepared_at=now,
            expiry_at=now + timedelta(hours=8),
            pickup_address='Banjara Banquet Gate 3, Road No. 1, Banjara Hills',
            city='Hyderabad',
            status='AVAILABLE'
        )

    def test_homepage_and_stats_endpoint(self):
        """Test Case 1: Verifies homepage renders correctly and live stats JSON endpoint responds."""
        response = self.client.get(reverse('donations:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rescue Food')
        self.assertContains(response, 'Hyderabadi Veg Dum Biryani')

        # Test live JSON API endpoint
        api_response = self.client.get(reverse('donations:api_stats'))
        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response['Content-Type'], 'application/json')
        data = api_response.json()
        self.assertIn('total_donations', data)
        self.assertGreaterEqual(data['total_donations'], 1)

    def test_user_authentication_and_role_routing(self):
        """Test Case 2: Verifies user login, credential verification, and role-based redirect."""
        # Test valid login
        login_success = self.client.login(username='chef_rajesh', password='password123')
        self.assertTrue(login_success)

        # Donor redirect should route to donor dashboard
        redirect_response = self.client.get(reverse('accounts:dashboard_redirect'), follow=True)
        self.assertEqual(redirect_response.status_code, 200)
        self.assertContains(redirect_response, 'Donor Management Portal')

        self.client.logout()

    def test_donation_creation_and_slug_converter(self):
        """Test Case 3: Tests creation of new donation with auto-slug and slug URL converter."""
        now = timezone.now()
        new_donation = Donation.objects.create(
            donor=self.donor_user,
            food_name='South Indian Masala Dosa',
            category='COOKED_MEALS',
            description='Hot crispy masala dosas with potato masala, sambar, and coconut chutney.',
            quantity=30.0,
            unit='plates',
            prepared_at=now,
            expiry_at=now + timedelta(hours=6),
            pickup_address='Annapurna Tiffin Center, Indiranagar',
            city='Bengaluru',
            status='AVAILABLE'
        )

        self.assertTrue(new_donation.slug)
        self.assertIn('south-indian-masala-dosa', new_donation.slug)

        # Test Slug path converter URL routing
        url = reverse('donations:donation_detail_slug', kwargs={'slug': new_donation.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'South Indian Masala Dosa')
        self.assertContains(response, '30')

    def test_database_driven_search_and_filtering(self):
        """Test Case 4: Tests database queries for search keywords and category filtering."""
        # Search by Indian keyword
        search_url = reverse('donations:donation_list') + '?q=Biryani'
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hyderabadi Veg Dum Biryani')

        # Filter by category
        cat_url = reverse('donations:donation_list') + '?category=COOKED_MEALS'
        cat_response = self.client.get(cat_url)
        self.assertEqual(cat_response.status_code, 200)
        self.assertContains(cat_response, 'Hyderabadi Veg Dum Biryani')

        # Search for non-existent item
        empty_search = reverse('donations:donation_list') + '?q=NonExistentPizzaItem'
        empty_response = self.client.get(empty_search)
        self.assertContains(empty_response, 'No Food Donations Found')

    def test_invalid_record_404_handling(self):
        """Test Case 5: Tests that accessing non-existent slug returns 404 error page."""
        invalid_url = reverse('donations:donation_detail_slug', kwargs={'slug': 'this-slug-does-not-exist-at-all'})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_food_request_and_delivery_lifecycle(self):
        """Test Case 6: End-to-end redistribution lifecycle (Request -> Accept -> Pickup -> Delivery)."""
        # 1. NGO submits request
        food_req = FoodRequest.objects.create(
            donation=self.donation,
            receiver=self.ngo_user,
            quantity_requested=40.0,
            message='Required for 40 children at Sneha Care Home in Jubilee Hills.',
            status='PENDING'
        )
        self.donation.status = 'REQUESTED'
        self.donation.save()
        self.assertEqual(food_req.status, 'PENDING')

        # 2. Donor accepts request
        food_req.status = 'APPROVED'
        food_req.save()
        self.donation.status = 'ACCEPTED'
        self.donation.save()

        delivery = Delivery.objects.create(
            food_request=food_req,
            delivery_status='ASSIGNED'
        )
        self.assertEqual(delivery.delivery_status, 'ASSIGNED')

        # 3. Volunteer claims and picks up
        delivery.mark_picked_up(volunteer_user=self.vol_user)
        self.assertEqual(delivery.delivery_status, 'PICKED_UP')
        self.assertEqual(delivery.volunteer, self.vol_user)
        self.donation.refresh_from_db()
        self.assertEqual(self.donation.status, 'COLLECTED')

        # 4. Volunteer marks delivered
        delivery.mark_delivered(remarks="Delivered piping hot biryani to Sister Sunita Reddy at Jubilee Hills gate.")
        self.assertEqual(delivery.delivery_status, 'DELIVERED')
        food_req.refresh_from_db()
        self.assertEqual(food_req.status, 'COMPLETED')
        self.donation.refresh_from_db()
        self.assertEqual(self.donation.status, 'DELIVERED')

    def test_role_dashboards_access(self):
        """Test Case 7: Verifies role-based authorization restrictions and dashboard views."""
        # Donor access
        self.client.login(username='chef_rajesh', password='password123')
        resp = self.client.get(reverse('donations:donor_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

        # NGO access
        self.client.login(username='sister_sunita', password='password123')
        resp_ngo = self.client.get(reverse('requests:ngo_dashboard'))
        self.assertEqual(resp_ngo.status_code, 200)
        resp_ngo_req = self.client.get(reverse('requests:ngo_my_requests'))
        self.assertEqual(resp_ngo_req.status_code, 200)
        self.client.logout()

        # Volunteer access
        self.client.login(username='ramesh_courier', password='password123')
        resp_vol = self.client.get(reverse('requests:volunteer_dashboard'))
        self.assertEqual(resp_vol.status_code, 200)
        self.client.logout()
