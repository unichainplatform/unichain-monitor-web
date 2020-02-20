from restapi.models import HostsModel, AccountModel


def host_parser():
    """
    :return:
        hosts: 服务器列表
        passwords: 密码列表
    """
    objs = HostsModel.objects.all()

    _hosts = [''.join([obj.user, '@', obj.ip, ':22']) for obj in objs]
    passwords = {''.join([obj.user, '@', obj.ip, ':22']) : obj.password for obj in objs}
    return _hosts, passwords


def account_reader():
    obj = AccountModel.objects.first()
    return obj.public_key, obj.private_key