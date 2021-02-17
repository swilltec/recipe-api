from django.test import TestCase
from django.contrib.auth import get_user_model


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
