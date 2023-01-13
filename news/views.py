from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import views, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import authentication, permissions
from .permissions import IsAuthorPermission, IsStaffPermission
from rest_framework import permissions

from .models import News, Comment, Status, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer, SatusSerializer, NewsStatusSerializer, CommentStatusSerializer

class PostPagePagination(PageNumberPagination):
    page_size = 3 #elemente na str


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_destroy(self, serializer):
        serializer.save(author=self.request.user.author)

    @action(methods=['GET', ], detail=True, permission_classes=[IsAuthorPermission])
    def slug(self, request, pk=None):
        serializer = NewsStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user.author,
                news=self.get_object()
            )
            return Response(f'{serializer.data}, Status added') #status=status.HTTP_201_CREATED)
        else:
            return Response(f"{serializer.data}, You already status")#status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentStatusSerializer
    permission_classes = [IsAuthorPermission]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_destroy(self, serializer):
        serializer.save(author=self.request.user.author)

    @action(methods=['GET', ], detail=True, permission_classes=[IsAuthorPermission])
    def slug(self, request, pk=None):
        serializer = CommentStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user.author,
                news=self.get_object()
            )
            return Response(f'{serializer.data}, Status added')  # status=status.HTTP_201_CREATED)
        else:
            return Response(f"{serializer.data}, You already status")  # status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorPermission]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )

class StatusesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = SatusSerializer
    permission_classes = [IsStaffPermission]

class StatusesRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = SatusSerializer
    permission_classes = [IsStaffPermission]

