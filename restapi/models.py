from django.db import models
from django.core.exceptions import ValidationError


class AccountModel(models.Model):
    public_key = models.CharField(max_length=500, blank=True, null=True)
    private_key = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and AccountModel.objects.exists():
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
            raise ValidationError('There is can be only one AccountModel instance')
        return super(AccountModel, self).save(*args, **kwargs)


class HostsModel(models.Model):
    ip = models.IPAddressField(max_length=200, blank=True, null=True, unique=True)
    user = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)