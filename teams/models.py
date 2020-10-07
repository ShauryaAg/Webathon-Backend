from django.db import models
from django.contrib.auth.models import AbstractUser

import hashlib


class Student(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    college = models.CharField(max_length=80)
    phone_no = models.CharField(max_length=10, unique=True, null=True)
    is_leader = models.BooleanField(default=False)
    username = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    idea = models.CharField(max_length=200)
    students = models.ManyToManyField(
        Student, blank=True, related_name='team')
    token = models.CharField(max_length=5, unique=True, null=True, blank=True)

    def __str__(self):
        return self.team_name

    def hash_Token(self):
        # Create a 256 byte long hash
        self.team_name_bytes = str.encode(self.team_name)
        self.token = hashlib.sha256(self.team_name_bytes).hexdigest()

        # Take only the first 5 letters of the hash
        self.token = self.token[:5]

    def save(self, *args, **kwargs):
        if not self.id:
            self.hash_Token()

        super().save(*args, **kwargs)


class Project(models.Model):
    project_name = models.CharField(max_length=50)
    git_url = models.URLField(max_length=200)
    deploy_link = models.URLField(max_length=200, null=True)
    description = models.TextField(null=True)
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, unique=True, related_name='team')

    def __str__(self):
        return self.project_name
