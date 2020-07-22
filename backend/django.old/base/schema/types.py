from django.contrib.auth.models import User
from graphene import types
from graphene_django.types import DjangoObjectType
from base.models import Profile, Post, Comment

class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class CommentListType(types.ObjectType):
    comments = types.List(types.NonNull(CommentType))
    total_results = types.Int()
    next_page = types.Boolean()


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class PostListType(types.ObjectType):
    posts = types.List(types.NonNull(PostType))
    total_results = types.Int()
    next_page = types.Boolean()