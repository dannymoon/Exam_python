from __future__ import unicode_literals
import re
from django.db import models

# Create your models here.
emailREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameREGEX = re.compile(r'^[A-Za-z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1 or len(postData['alias']) < 1 or len(postData['email']) < 1 or len(postData['password']) < 1 or len(postData['confirm_password']) < 1:
            errors["all"] = "All fields must be filled"
            return errors
        if len(postData['name']) < 3:
            errors["name"] = "Name should be more than 2 characters"
        if len(postData['alias']) < 3:
            errors["alias"] = "Alias should be more than 2 characters"
        if not nameREGEX.match(postData['name']):
            errors["name"] = "name fields must be letter characters only"
        if not nameREGEX.match(postData['alias']):
            errors["alias"] = "alias fields must be letter characters only"
        if not emailREGEX.match(postData['email']):
            errors["email"] = "Email must be in proper format"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Password must match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}>".format(self.name)

class QuoteManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors["author"] = "Quoted by must be more than 3 characters"
        if len(postData['intext']) < 10:
            errors["intext"] = "Message by must be more than 10 characters"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length=255)
    intext = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="quotes_posted")
    favored_by = models.ManyToManyField(User, related_name="quotes_favored")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    def __repr__(self):
        return "<Quote object: {}>".format(self.author)