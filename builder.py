from fabric.api import task, env, run, put, settings, cd, hide, execute, parallel
from utils import host_parser, account_reader


hosts, passwords = host_parser()
public_key, private_key = account_reader()

env.hosts.extend(hosts)
env.passwords = passwords


def install_go():
    run('wget https://dl.google.com/go/go1.13.7.linux-amd64.tar.gz')
    with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
    ):
        run("tar -C /usr/local -zxvf  go1.13.7.linux-amd64.tar.gz")
    run("echo 'export GOROOT=/usr/local/go' >> /etc/profile")
    run("echo 'export PATH=$PATH:$GOROOT/bin' >> /etc/profile")
    run("source /etc/profile")
    run("go version")


def initial():
    run('apt update')
    run('apt install -y git jq moreutils screen')
    return


def check_go():
    with settings(warn_only=True):
        result = run('go version')
    if result.return_code != 0:
        return False
    return True


def check_unichain_installed():
    with settings(warn_only=True):
        result = run('~/unichain/build/bin/uni version')
    if result.return_code != 0:
        return False
    return True


def check_unichain_running():
    with settings(warn_only=True):
        with cd('~/unichain/build/bin'):
            mined_log = run('tail -1 node1.log')
            sync_log_2 = run('tail -1 node2.log')
            sync_log_3 = run('tail -1 node3.log')

    if mined_log.return_code != 0 or sync_log_2.return_code != 0 or sync_log_3.return_code != 0:
        return False
    if "Mined new block" not in mined_log:
        return False
    if "Imported new chain segment" not in sync_log_2:
        return False
    if "Imported new chain segment" not in sync_log_3:
        return False
    return True


def install_unichain():
    run("git clone https://github.com/unichainplatform/unichain.git ~/unichain")
    with cd('~/unichain'):
        run("make fmt")
        run("make all")


def make_unichain_run():
    run("ps -A | grep uni | awk '{print $1}' | xargs -n1")
    with cd('~/unichain/build/bin'):
        run("""jq '.allocAccounts[0].pubKey="{}"' ../genesis.json | sponge ../genesis.json""".format(public_key))
        run("""jq '.config.bootnodes=["fnode://a85ccab0374c60ddea0a63b521ae3f8475100ff4e116090d6798a8618ceea193f5b7deffc14627b2f61bc374336983f6a6c6ed979478590d49906e8ce6041a18@127.0.0.1:2018"]' ../genesis.json | sponge ../genesis.json""")

        run("touch privateKey.txt")
        run("""echo {} > privateKey.txt""".format(private_key))
        # node 8545
        run("nohup ./uni --genesis=../genesis.json --datadir=./data/node1 --miner_start --contractlog --http_modules=fee,miner,dpos,account,txpool,uni &>node1.log & sleep 5; exit 0", warn_only=True)
        run("nohup ./uni --genesis=../genesis.json --datadir=./data/node2 --p2p_listenaddr :2019  --http_host 0.0.0.0 --http_port 8080 --ws_port 8081 --contractlog --http_modules=fee,miner,dpos,account,txpool,uni &> node2.log & sleep 5; exit 0", warn_only=True)
        run("nohup ./uni --genesis=../genesis.json --datadir=./data/node3 --p2p_listenaddr :2020  --http_host 0.0.0.0 --http_port 8090 --ws_port 8091 --contractlog --http_modules=fee,miner,dpos,account,txpool,uni &> node3.log & sleep 5; exit 0", warn_only=True)
        run('./uni miner -i ./data/node1/uni.ipc setcoinbase "unichain.founder" privateKey.txt')
        run('rm privateKey.txt')


@task
@parallel(pool_size=100)
def build():
    initial()
    if not check_go():
        install_go()

    if not check_unichain_installed():
        install_unichain()

    if not check_unichain_running():
        make_unichain_run()