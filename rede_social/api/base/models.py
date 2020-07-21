from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import enums

class BaseModel(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Profile(BaseModel):
    class Meta:
        verbose_name = "perfil de usuário"
        verbose_name_plural = "perfis de usuário"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField("verificado", default=False)
    # hometown = models.CharField("cidade natal", max_length=25)
    # city = models.CharField("cidade natal", max_length=25)
    # birthday = models.DateField("data de nascimento", null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return self.user.username


class Post(BaseModel):
    class Meta:
        verbose_name = "postagem"
        verbose_name_plural = "postagens"

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="autor", related_name="posts_author")
    description = models.TextField("descrição", null=False, blank=False)
    like = models.ManyToManyField(Profile, blank=True, verbose_name="curtida", related_name="posts_like")


class Product(BaseModel):
    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    price = models.DecimalField("preço", max_digits=13, decimal_places=2, default=0)
    free_ship = models.BooleanField("frete grátis", default=False)
    installment = models.PositiveSmallIntegerField("parcelas", default=0)
    stock = models.PositiveSmallIntegerField("estoque", default=0)
    category = models.CharField("categoria", max_length=20, choices=enums.ProductCategories)


class Comment(BaseModel):
    class Meta:
        verbose_name = "comentário"
        verbose_name_plural = "comentários" 

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="autor", related_name="comments_author")
    text = models.TextField("comentário", null=False, blank=False)
    like = models.ManyToManyField(Profile, blank=True, verbose_name="curtida", related_name="comments_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="postagem", related_name="comments")
