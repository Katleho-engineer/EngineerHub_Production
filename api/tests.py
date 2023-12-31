# from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from django.urls import reverse

from handle_app.models import User, Topic


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'Password@123',
            'password2': 'Password@123',
        }

        url = reverse('register-api')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='one@gmail.com', password='Password@123', email='one@gmail.com')

    def test_login(self):
        data = {
            'username': 'one@gmail.com',
            'password': 'Password@123',
            'email': 'one@gmail.com',
        }

        url = reverse('login-api')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username='one@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('logout-api')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TopicTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='one@gmail.com', password='Password@123', email='one@gmail.com')
        self.token = Token.objects.get(user__username='one@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.topic = Topic.objects.create(name='Testing')

    def test_topic_create(self):
        data = {
            'name': 'Topic name'
        }
        url = reverse('topics-api')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_topic_individual(self):
        url = reverse('topic-api', args=(self.topic.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MessageTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='one@gmail.com', password='Password@123', email='one@gmail.com')
        self.token = Token.objects.get(user__username='one@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.topic = Topic.objects.create(name='Testing')

    def test_messages_get(self):
        url = reverse('message-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_room_messages_get(self):
        url = reverse('room-messages-api', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''
    def test_room_messages_create(self):
        data = {
            'body': 'Topic name',
            'room': 'Aerospace'
        }
        url = reverse('room-messages-api', args=('1',))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''

    def test_user_messages_get(self):
        url = reverse('user-messages-api', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='one@gmail.com', password='Password@123', email='one@gmail.com')
        self.token = Token.objects.get(user__username='one@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_rooms_get(self):
        url = reverse('rooms-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''
    def test_room_individual_get(self):
        url = reverse('room-api', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    '''