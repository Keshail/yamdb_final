from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email__exact=value).exists():
            raise serializers.ValidationError('Duplicate email')
        return value

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'bio')


class SignupSerializer(UserSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" can not used for username')
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        code = data['confirmation_code']
        if not default_token_generator.check_token(user.username, code):
            raise serializers.ValidationError('Wrong confirmation code.')
        return data

    class Meta:
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(max_value=10, min_value=1)
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        title = get_object_or_404(
            Title,
            id=self.context['request'].parser_context['kwargs']['title_id'],
        )
        author = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=author, title=title).exists()
        ):
            raise serializers.ValidationError(
                'Дважды оставить отзыв на одно произведение нельзя.')
        return data

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
