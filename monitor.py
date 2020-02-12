from fabric.api import task, env, run, put, settings, cd, hide, execute, parallel
from utils import host_parser
import re

hosts, passwords = host_parser()

env.hosts.extend(hosts)
env.passwords = passwords

mined_list = []
sync_list = []
item = {}


def _monitor():
    with cd('~/uni/build/bin'):
        logs = []
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
    ):
            mined_log =run('tail -1 node1.log')
            sync_log_2 = run('tail -1 node2.log')
            sync_log_3 = run('tail -1 node3.log')

            if "Mined new block" in mined_log:
                mined_number = re.findall('number=(\d*)', mined_log)[0]
                mined_list.append(mined_number)
                logs.append({
                    "status": 1, "number": mined_number, "type": "node1"
                })
            else:
                logs.append({
                    "status": 0, "reason": mined_log, "type": "node1"
                })

            if "Imported new chain segment" in sync_log_2:
                sync_number_2 = re.findall('number=(\d*)', mined_log)[0]
                sync_list.append(sync_number_2)
                logs.append({
                    "status": 1, "number": mined_number, "type": "node2"
                })
            else:
                logs.append({
                    "status": 0, "reason": sync_log_2, "type": "node2"
                })

            if "Imported new chain segment" in sync_log_3:
                sync_number_3 = re.findall('number=(\d*)', mined_log)[0]
                sync_list.append(sync_number_3)
                logs.append({
                    "status": 1, "number": mined_number, "type": "node3"
                })
            else:
                logs.append({
                    "status": 0, "reason": sync_log_3, "type": "node3"
                })
    item[env.host_string] = logs


def monitor_result():
    global mined_list
    global sync_list
    global item
    execute(_monitor)
    tmp_sync = sync_list
    tmp_mined = mined_list
    tmp_item = item

    sync_list = []
    mined_list = []
    item = {}
    return {
        "max_sync_number": max(tmp_sync),
        "max_mined_number": max(tmp_mined),
        "data": tmp_item
    }