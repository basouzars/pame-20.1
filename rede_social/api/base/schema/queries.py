import graphene
from base.schema.types import UserType

class Queries(object):
    user = graphene.Field(UserType)
    def resolve_user(self, info):
        return info.context.user