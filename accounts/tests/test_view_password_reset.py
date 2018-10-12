from django.contrib.auth import views as auth_views
from django.urls import resolve, reverse
from django.test import TestCase

class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)
    
    def 