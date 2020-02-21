from django.db import models
from django.core.exceptions import ValidationError


class Accounts(models.Model):
    public_key = models.CharField(max_length=500, blank=True, null=True)
    private_key = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and Accounts.objects.exists():
            raise ValidationError('There is can be only one AccountModel instance')
        return super(Accounts, self).save(*args, **kwargs)


class Hosts(models.Model):
    status_choice = (
        (0, 'initial'),
        (1, 'dependent'),
        (2, 'golang'),
        (3, 'unichain'),
        (4, 'running'),
        (-1, 'fail'),
    )
    ip = models.CharField(max_length=200, blank=True, null=True, unique=True)
    user = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=status_choice, default=0)