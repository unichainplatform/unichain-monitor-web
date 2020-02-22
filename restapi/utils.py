from restapi.models import Hosts, Accounts


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
    if obj:
        return obj.public_key, obj.private_key
    else:
        return None, None