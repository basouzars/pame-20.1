import graphene
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required
from base.schema.types import UserType, PostListType, CommentListType
from base.models import Post, Comment


POST_LIST_SIZE = 10
COMMENT_LIST_SIZE = 5


class Queries(object):
    user = graphene.Field(UserType)
    posts_list = graphene.Field(PostListType, page=graphene.Int())
    comments_list = graphene.Field(CommentListType, page=graphene.Int(), post_id=graphene.Int())

    @login_required
    def resolve_user(self, info):
        return info.context.user

    def resolve_posts_list(self, info, page = 1):
        posts = Post.objects.all().order_by('-creation_date')
        paginator = Paginator(posts, POST_LIST_SIZE)
        page = paginator.get_page(page)
        return PostListType(posts=page, total_results=paginator.count, next_page=page.has_next())

    def resolve_comments_list(self, info, post_id, page = 1):
        comments = Comment.objects.filter(post=post_id).order_by('-creation_date')
        paginator = Paginator(comments, COMMENT_LIST_SIZE)
        page = paginator.get_page(page)
        return CommentListType(comments=page, total_results=paginator.count, next_page=page.has_next())

