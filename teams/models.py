from django.db import models
from django.contrib.auth.models import AbstractUser

import hashlib


class Student(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    college = models.CharField(max_length=80)
    phone_no = models.CharField(max_length=10)
    is_leader = models.BooleanField(default=False)
    username = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    idea = models.CharField(max_length=200)
    project_link = models.URLField(max_length=200, blank=True)
    students = models.ManyToManyField(
        Student, blank=True)
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
    github_url = models.URLField(max_length=200, null=True)
    link = models.URLField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
