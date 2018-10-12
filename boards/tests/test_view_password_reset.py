from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase

class PasswordResetTests(TestCase):
    def setUp(self):
        '''
        setup function
        '''
        url = reverse('password_reset')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        '''
        Checks password_reset status code
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        '''
        Checks if '/reset/' returns
         the 'password reset' page
        ''' 
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class,
         auth_views.PasswordResetView)
    
    def test_csrf(self):
        '''
        Checks if csrf middleware token is generated
        '''
        self.assertContains(self.response,
         'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        '''
        Checks if password_reset page contains
         the 'password_reset' view
        ''' 
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
    
    def test_form_inputs(self):
        '''
        The view must contain two input csrf and email
        '''

        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email')

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        '''
        Setting up a test case for the 'Password Reset'
        '''
        email = 'shaz_swain@gmail.com'
        User.objects.create_user(username="shaz_swa in")
        url = reverse('password_reset')
        self.response = self.client.post(url,
         {'email': email})

    def test_redirection(self):
        '''
        A valid form submission should redirects
         the user to 'password_reset_done' view
        '''
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        '''
        Checks if password reset email has been sent
        '''
        self.assertEqual(1, len(mail.outbox))

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        '''
        Setting up an test case email that
         does not exits in the database
        '''
        url = reverse('password_reset')
        self.response = self.client.post(url,
         {'email': 'false_email@somemail.com'})
    
    def test_redirection(self):
        '''
        Even invalid emails in the database redirects
         the user to 'password_reset_done' view
        '''
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        '''
        Checks if email has NOT been sent
        '''
        self.assertEqual(0, len(mail.outbox)) 