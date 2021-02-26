from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttr(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return objects for the current authenticated use only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    """manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    """manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """manage recipe in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """return objects for the current authenticated use only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)