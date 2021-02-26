from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that a login is required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """test the authorized user ingredients api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """test retrieving ingredients"""
        Ingredient.objects.create(user=self.user, name='Vegan')
        Ingredient.objects.create(user=self.user, name='Dessert')

        res = self.client.get(INGREDIENTS_URL)

        Ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(Ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """test that ingredients returned are for the authenticated user"""

        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Honey')
        ingredient = Ingredient.objects.create(
            user=self.user,
            name="Sweet food")

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """test creating a new ingredient"""
        payload = {'name': 'Test ingredient'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """test creating a new ingredient with invalid payload"""

        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
