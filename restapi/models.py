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


def host_parser():
    """
    :return:
        hosts: 服务器列表
        passwords: 密码列表
    """
    objs = Hosts.objects.all()

    _hosts = [''.join([obj.user, '@', obj.ip, ':22']) for obj in objs]
    passwords = {''.join([obj.user, '@', obj.ip, ':22']) : obj.password for obj in objs}
    return _hosts, passwords


def account_reader():
    obj = Accounts.objects.first()
    return obj.public_key, obj.private_key