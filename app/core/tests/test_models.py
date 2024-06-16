from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal
from core import models
class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@gmail.com"
        password = 'testpass234'
        user = get_user_model().objects.create_user(
            email = email ,
            password = password
        )
        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com' , 'test1@example.com'  ],
            ['Test2@EXAMPLE.com' , 'Test2@example.com'  ],
            ['TEST3@EXAMPLE.com' , 'TEST3@example.com'  ],
            ['test4@example.com' , 'test4@example.com'  ],
            
        ]
        for email , expected_email in sample_emails:
            user = get_user_model().objects.create_user(email = email , password ="test123pass")
            self.assertEqual(user.email , expected_email)
    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')
    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            email = "superuser@gmail.com",
            password = "test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    def test_create_recipe(self):
        user = get_user_model().objects.create_superuser(
            email = "superuser@gmail.com",
            password = "test123"
        )
        recipe = models.Recipe.objects.create(
            user= user,
            title = 'sample recipe name',
            time_minutes = 5,
            price = Decimal('5.50'),
            description = "sample recipe description"
        )
        self.assertTrue(recipe.title == str(recipe))
    def test_create_tag(self):
        user = get_user_model().objects.create_user(
            email = "superuser@gmail.com",
            password = "test123"
        )
        tag = models.Tag.objects.create(user= user , name="tag1")
        self.assertEqual(str(tag),tag.name)
    def test_create_ingredient(self):
        user = get_user_model().objects.create_user(
            email = "superuser@gmail.com",
            password = "test123"
        )
        tag = models.Ingredient.objects.create(user= user , name="ing1")
        self.assertEqual(str(tag),tag.name)
    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self , mock_uuid):
        """Testing generating image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None,'example.jpg')
        self.assertEqual(file_path , f'uploads/recipe/{uuid}.jpg')
        
        