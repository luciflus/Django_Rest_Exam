"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from rest_framework import permissions


from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account import views as acc_view
from news import views as news_view

acc_router = DefaultRouter()
acc_router.register('register', acc_view.AuthorViewSet)

posts_router = DefaultRouter()
posts_router.register('news', news_view.NewsViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="exam",
      default_version='v-0.01-beta',
      description="exam",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="sultanu@inbox.ru"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include(acc_router.urls)),
    path('api/account/token', obtain_auth_token),
    path('api/auth/', include('rest_framework.urls')),

    path('api/', include(posts_router.urls)),
    path('api/news/<int:news_id>/comments/', news_view.CommentListCreateAPIView.as_view()),
    path('api/news/<int:news_id>/comments/<int:pk>/', news_view.CommentRetrieveUpdateDestroyAPIView.as_view()),

    path('api/news/<int:news_id>/slug/', news_view.CommentListCreateAPIView.as_view()),
    #path('api/news/<int:news_id>/comments/<int:comment_id>/slug/', news_view.CommentViewSet.as_view()),

    path('api/statuses/', news_view.StatusesListCreateAPIView.as_view()),
    path('api/statuses/<int:pk>/', news_view.StatusesRetrieveUpdateDestroyAPIView.as_view()),

    # documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),
]
