import graphene
import graphql_jwt
from base.schema.mutations import Mutations
from base.schema.queries import Queries


class Query(Queries, graphene.ObjectType):
    pass

class Mutation(Mutations, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
