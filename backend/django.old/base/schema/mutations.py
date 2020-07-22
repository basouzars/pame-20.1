import graphene
from graphene_django.types import ErrorType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from django.shortcuts import get_object_or_404
from django.apps import apps
from base import forms
from base.models import Comment, Post

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


class CreatePost(graphene.Mutation):
    class Arguments:
        description = graphene.String()

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, description):
        author = info.context.user.profile
        post = Post.objects.create(author=author, description=description)
        return CreatePost(ok=True)


class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        post_id = graphene.Int()

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, post_id, text):
        author = info.context.user.profile
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment.objects.create(author=author, post=post, text=text)
        return CreateComment(ok=True)


class LikeObject(graphene.Mutation):
    class Arguments:
        model = graphene.String()
        id = graphene.Int()

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, model, id):
        user = info.context.user.profile
        
        if model == 'post' or model == 'comment':
            Model = apps.get_model('base', model)
            obj = get_object_or_404(Model, pk=id)
            obj.like.add(user)
            return LikeObject(ok=True)
        
        return LikeObject(ok=False)



class DeleteObject(graphene.Mutation):
    class Arguments:
        model = graphene.String()
        id = graphene.Int()

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, model, id):
        allow = False
        user = info.context.user.profile

        if model == "profile" and user == id:
            allow = True
        
        if model == "post":
            post = get_object_or_404(Post, pk=id)
            if user == post.author:
                allow = True
        
        if model == "comment":
            comment = get_object_or_404(Comment, pk=id)
            if user == comment.author or user == comment.post.author:
                allow = True

        if allow:
            Model = apps.get_model('base', model)
            Model.objects.filter(pk=id).delete()
            return DeleteObject(ok=True)
        
        return DeleteObject(ok=False)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    like_object = LikeObject.Field()
    delete_object = DeleteObject.Field()
