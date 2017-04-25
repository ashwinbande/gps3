from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_revocation_manager = models.BooleanField(default=False)
    is_opening_manager = models.BooleanField(default=False)
    is_group_manager = models.BooleanField(default=False)
    Ai = models.CharField(max_length=1024, null=True, blank=True, unique=True)
    Ei = models.CharField(max_length=1024, null=True, blank=True, unique=True)
    Xi = models.CharField(max_length=1024, null=True, blank=True)
    sign_created = models.BooleanField(default=False, blank=True)
    is_revoked = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.username


class Messeges(models.Model):
    title = models.CharField(max_length=1024)
    text = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    C = models.CharField(max_length=1024, )
    S1 = models.CharField(max_length=1024, )
    S2 = models.CharField(max_length=1024, )
    S3 = models.CharField(max_length=1024, )
    T1 = models.CharField(max_length=1024, )
    T2 = models.CharField(max_length=1024, )
    T3 = models.CharField(max_length=1024, )

    def __str__(self):
        return self.title

class Revocation_list(models.Model):
    Ai = models.CharField(max_length=1024, null=True, blank=True, unique=True)
    Ei = models.CharField(max_length=1024, null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.Ai)

class revocation_requests(models.Model):
    Ai = models.CharField(max_length=1024, null=True, blank=True)
    Ei = models.CharField(max_length=1024, null=True, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.completed)