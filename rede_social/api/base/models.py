from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return self.user.username
