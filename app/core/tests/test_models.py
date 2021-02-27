from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test_user@gmail.com', password='testpass'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    email = "test@Gmail.com"
    password = "12345678"

    def setUp(self):
        get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email sucessfully"""
        user = get_user_model().objects.get(email="test@gmail.com")
        self.assertTrue(user)
        self.assertTrue(user.check_password(self.password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        self.assertTrue(get_user_model().objects.get(email="test@gmail.com"))

    def test_new_user_invalid_email(self):
        """test creating a new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, self.password)

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test2@gmail.com',
            self.password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """test the integrient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Peper'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_Recipe_str(self):
        """test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='peper soup',
            time_min=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """test that image is saved in the correct location"""

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'image.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
