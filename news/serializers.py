from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import News, Comment, Status, NewsStatus, CommentStatus
from account.models import Author

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author', 'news']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'news']

class SatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class NewsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsStatus
        fields = '__all__'
        #read_only_fields = ['author', 'status', 'news']

class CommentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentStatus
        fields = '__all__'
        read_only_fields = ['author', 'status', 'comment']