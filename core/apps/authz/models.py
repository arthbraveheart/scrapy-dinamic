from django.db import models
from django.contrib.auth.models import AbstractUser


class LowProfile(AbstractUser):
    phone_number = models.CharField(max_length=17, )
    first_name   = models.CharField(max_length=17, default="emptyField")
    last_name    = models.CharField(max_length=17, default="emptyField")
    role_name = models.CharField(max_length=17, default="emptyField")


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_manager(self):
        return self.groups.filter(name='Manager').exists()

    @property
    def complete_name(self):
        return f'{self.first_name} {self.last_name}'
