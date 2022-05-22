from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()
v1_router.register('categories', views.CategoryViewSet, basename='categories')
v1_router.register('genres', views.GenreViewSet, basename='genres')
v1_router.register('titles', views.TitleViewSet, basename='titles')
v1_router.register('users', views.UsersViewSet, basename='users')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   views.ReviewsViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/users/me/', views.current_user_detail),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', views.get_tokens_for_user),
    path('v1/auth/signup/', views.signup),
]
