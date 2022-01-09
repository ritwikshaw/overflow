from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, email, password):
        new = self.create_user(
            first_name=first_name,
            email=email,
            password=password,
        )
        new.is_active = True
        new.is_staff = True
        new.is_superuser = True
        new.save(using=self._db)
        return new


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def get_full_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Qvote(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Qdown(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Avote(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Adown(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    des = models.CharField(max_length=200)
    questionid = models.CharField(max_length=10)
    positivevote = models.ManyToManyField(Avote, related_name="admin_Avote")
    negativevote = models.ManyToManyField(Adown, related_name="admin_Adown")
    acomment = models.ManyToManyField(Comment, related_name="admin_Comment")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    des = models.CharField(max_length=200)
    tags = TaggableManager()
    answer = models.ManyToManyField(Answer, related_name="admin_Answer")
    positivevote = models.ManyToManyField(Qvote, related_name="admin_qvote")
    negativevote = models.ManyToManyField(Qdown, related_name="admin_Qdown")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
