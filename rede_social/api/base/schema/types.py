from django.contrib.auth.models import User
from graphene import types
from graphene_django.types import DjangoObjectType
from base.models import Profile

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('first_name', 'profile')


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('verified',)