from fabric.api import task, env, run, put, settings, cd, hide, execute
from utils import host_parser
from termcolor import colored

hosts, passwords = host_parser()

env.hosts.extend(hosts)
env.passwords = passwords


def _monitor():
    r = list()

    with cd('~/fractal/build/bin'):
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
    ):
            r.append((8545, run('tail -1 8545.log')))
            r.append((8547, run('tail -1 8547.log')))
            r.append((8549, run('tail -1 8549.log')))
            r.append((8551, run('tail -1 8551.log')))
    for v in r:
        level = v[1].split(' ', 1)[0]
        text = v[1].split(' ', 1)[1]
        print(
            colored('[' + env.host_string + ']', 'blue'),
            colored('[http_port@' + str(v[0]) + ']', 'green'),
            colored(level, 'red'), text
        )
    return r


def monitor_result():
    return execute(_monitor)