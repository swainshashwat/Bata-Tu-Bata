from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post

# Create your tests here.

class HomeTests(TestCase):
    
    def test_home_view_status_code(self):
        '''
        Testing the status code:
        status code '200' is success
        '''
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

class BoardTopicsTests(TestCase):
    
    def setUp(self):
        '''
        Temporary Board instance for running tests.
        '''
        Board.objects.create(name='Django',
         description='Django board.')
    
    def test_board_topics_view_success_status_code(self):
        '''
        Testing for page found.
        '''
        url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        '''
        Testing for page NOT found.
        '''
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_url_resolves_board_topics_view(self):
        '''
        Checks if Django is using the current view function.
        '''
        view = resolve('/boards/1/')

        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        '''
        Checks if link to the home(Board) page works
        and tests the view to the required navigation links.
        '''
        board_topics_url = reverse('board_topics',
         kwargs={'pk':1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic',
         kwargs={'pk':1})
        response = self.client.get(board_topics_url)

        self.assertContains(response,
         'href="{0}"'.format(homepage_url))
        self.assertContains(response, 
         'href="{0}"'.format(new_topic_url))


class HomeTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name='Django',
         description='Django Board')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics',
        kwargs={'pk': self.board.pk})
        self.assertContains(self.response,
         'href="{0}"'.format(board_topics_url))

class NewTopicTests(TestCase):
    def setUp(self):
        '''
        Temporary Board instance for running tests.
        '''
        Board.objects.create(name='Django',
         description='Django: Test Database')
        User.objects.create_user(username='john',
        email='john@doe.com', password='123')
    
    def test_new_topic_view_success_status_code(self):
        '''
        checks if the request to the view is successful.
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_new_topic_view_not_found_status_code(self):
        '''
        checks if view raises 404 error.
        '''
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        '''
        checks if the right view is being used.
        '''
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        '''
        checks if the page navigates
         back to the list of topics.
        '''
        new_topic_url = reverse('new_topic',
         kwargs={'pk': 1})
        board_topics_url = reverse('board_topics',
         kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response,
         'href="{0}"'.format(board_topics_url))
    
    def test_csrf(self):
        '''
        checks if our HTML file contains csrf token.
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response,
        'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        '''
        checks if view created a Topic and a Post instance.
        '''
        url = reverse('new_topic',
        kwargs={'pk':1})
        data = {
            'subject' : 'Test title',
            'message' : 'Random message ABC.'
        }

        response = self.client.post(url, data)

        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        Expected behavior: show the form again
         with validation errors.
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        Expected behavior: show the form again
         with validation errors.
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
