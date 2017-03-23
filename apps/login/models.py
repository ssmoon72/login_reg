from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REG = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# PASSWORD_REG = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password):
        error_messages = []
        if len(first_name) < 2:
            error_messages.append('First Name Too Short')
        elif not first_name.isalpha():
            error_messages.append('First Name can only contain letters')
        if len(last_name) < 2:
            error_messages.append('Last Name Too Short')
        elif not first_name.isalpha():
            error_messages.append('Last Name can only contain letters')
        if not EMAIL_REG.match(email):
            error_messages.append('Email Invalid')
        # if not PASSWORD_REG.match(password):
        #     error_messages.append('Invalid Password')
        if password != confirm_password:
            error_messages.append('Password and Confirm Password must match')
        if error_messages == []:
            password = password.encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            user = User.usermanager.create(first_name=first_name, last_name=last_name, email=email, password=password)
            return { 'theUser': user }
        else:
            return {'errors': error_messages }

    def login(self, email, password):
        error_messages = []
        if self.filter(email = email).exists():
            password = password.encode('utf-8')
            stored_pw = User.usermanager.get(email=email).password
            if bcrypt.hashpw(password, stored_pw.encode('utf-8')) != stored_pw:
                error_messages.append('password incorrect')
            else:
                user = self.get(email=email)
        else:
            error_messages.append('email incorrect')
        if error_messages == []:
            return {'theUser': user}
        else:
            return {'errors': error_messages}





class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    usermanager = UserManager()
