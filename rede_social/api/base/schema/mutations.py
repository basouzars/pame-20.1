import graphene
from graphene_django.types import ErrorType
from graphql_jwt.decorators import login_required, user_passes_test
from graphql_jwt.shortcuts import get_token
from base import forms


class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()
    token = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, first_name, email, password):
        user_form = forms.UserForm({
            'first_name': first_name,
            'username': email,
            'email': email,
            'password': password,
        })

        if not user_form.is_valid():
            errors = user_form.errors

            email_errors = errors.get('email', [])
            username_errors = errors.pop('username', [])
            errors['email'] = email_errors + username_errors

            errors = ErrorType.from_errors(errors)
            return CreateUser(ok=False, errors=errors)

        user = user_form.save()
        token = get_token(user)
        return CreateUser(ok=True, token=token)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
