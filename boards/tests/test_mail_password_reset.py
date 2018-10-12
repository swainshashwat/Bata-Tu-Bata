from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordResetMailTests(TestCase):
    def setUp(self):
        '''
        Create a Test Case instace
        '''
        User.objects.create_user(username='shaz',
        email='shazman@gmail.com', password='pass123')

        self.response = self.client.post(
            reverse('password_reset'), 
            {'email': 'shazman@gmail.com'})
            
        self.email = mail.outbox[0]

    def test_email_subject(self):
        '''
        Checks the subject of the email
        '''
        self.assertEqual(
            '[KHATTI] Please reset your password',
             self.email.subject)
    
    def test_email_body(self):
        '''
        Checks if the correct token is generated
        and sent to the email of the specific user
        '''
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse(
            'password_reset_confirm', kwargs={
                'uidb64': uid,
                'token': token 
            })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('shaz', self.email.body)
        self.assertIn('shazman@gmail.com', self.email.body)

    def test_email_to(self):
        '''
        Checks the receiver of the email
        '''
        self.assertEqual(['shazman@gmail.com',], self.email.to)