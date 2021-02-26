from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """create and return a sample recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_min': 10,
        'price': 5.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipesApiTests(TestCase):
    """test the publicly available Recipes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that a login is required for retrieving Recipes"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """test the authorized user Recipes api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_Recipes(self):
        """test retrieving Recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        Recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(Recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_Recipes_limited_to_user(self):
        """test that Recipes returned are for the authenticated user"""

        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    # def test_create_Recipe_successful(self):
    #     """test creating a new Recipe"""
    #     payload = {'name': 'Test Recipe'}
    #     self.client.post(RECIPES_URL, payload)

    #     exists = Recipe.objects.filter(
    #         user=self.user,
    #         name=payload['name']
    #     ).exists()
    #     self.assertTrue(exists)

    # def test_create_Recipe_invalid(self):
    #     """test creating a new Recipe with invalid payload"""

    #     payload = {'name': ''}
    #     res = self.client.post(RECIPES_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
