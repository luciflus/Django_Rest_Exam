from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import AuthorSerializer
from .models import Author, User

class AuthorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
