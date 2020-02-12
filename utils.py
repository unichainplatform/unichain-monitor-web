import json


def host_parser():
    """
    从settings文件中解析服务器信息

    :return:
        hosts: 服务器列表
        passwords: 密码列表
    """
    with open('hosts.json', 'r') as data:
        json_data = json.loads(data.read())
        hosts = list(json_data.keys())
        _hosts = [''.join([json_data[host]['user'], '@', host, ':22']) for host in hosts]
        passwords = {''.join([json_data[host]['user'], '@', host, ':22']) : json_data[host]['password'] for host in hosts}
        return _hosts, passwords