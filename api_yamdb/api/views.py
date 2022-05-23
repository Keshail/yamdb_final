from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import IsAdmin, IsAuthorModeratorAdminOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)

ROLENAME = 'user'


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAdmin | ReadOnly, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', '=slug']
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | ReadOnly, )
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'id'
    )
    filterset_class = TitleFilter
    ordering_field = ['name']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')),
            author=self.request.user,
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title_id=title_id, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id')),
        )


@api_view(['GET', 'PATCH'])
def current_user_detail(request):
    me = get_object_or_404(User, username=request.user)
    if request.method == 'GET':
        serializer = UserSerializer(me)
        return Response(serializer.data)
    serializer = UserSerializer(me, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if me.is_user:
        serializer.save(role=ROLENAME)
    else:
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    email_to = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user, created = User.objects.get_or_create(
        username=username,
        email=email_to
    )

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Confirmation code',
        f'Код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email_to],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    return str(RefreshToken.for_user(user))
