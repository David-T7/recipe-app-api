from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL  = reverse('user:create')

def create_user(**parms):
    # create and return user
    return get_user_model().objects.create_user(**parms)

class PublicApiTests(TestCase):
    # test the public features of the api
    def setUP(self):
        self.client = APIClient
    def test_create_user_success(self):
        payload ={
            'email':'test@gmail.com',
            'password':'test123',
            'name':'Test user'
        }
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password' , res)
    def test_user_with_email_exits_error(self):
        payload ={
            'email':'test@gmail.com',
            'password':'test123',
            'name':'Test user'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
    def test_password_too_short_error(self):
        payload ={
            'email':'test@gmail.com',
            'password':'12',
            'name':'Test user'
        }
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
        user_exits = get_user_model().objects.filter(email = payload['email'])
        self.assertFalse(user_exits)
        
        
        
        
        
     