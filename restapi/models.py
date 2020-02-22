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
        (0, 'has no start'),
        (1, 'initial'),
        (2, 'install dependent'),
        (3, 'install golang'),
        (4, 'build unichain'),
        (5, 'done'),
        (-1, 'fail'),
    )
    ip = models.CharField(max_length=200, blank=True, null=True, unique=True)
    user = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=status_choice, default=0)