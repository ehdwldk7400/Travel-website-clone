from django.db import models


class Account(models.Model):
    username         = models.CharField(max_length=50, null=True)
    email            = models.EmailField(max_length=100, unique=True, null=True)
    password         = models.CharField(max_length=400)
    phone            = models.IntegerField(null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'
