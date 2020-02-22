unichain 管理后台
===
virtualenv
---
```
// install pip3
apt install python3-pip
// instal virtualenv
pip3 install virtualenv
//create virtualenv
virtualenv -p python3 venv
//use virtualenv
source venv/bin/active
```
dependent
---
```shell script
cd <project>
pip3 install -r requirements.txt
apt install redis-server
[test redis]
>>> redis-cli ping
>>> PONG
apt install nginx
```
celery
---
```
```
nginx & uwsgi
---
```shell script
# [OPTIONAL!]
# [test if uwsgi works]
# uwsgi --http :8000 --module web.wsgi
# [then curl localhost:8000 and verify if result is 200/OK]
# [NOW CTRL+C TO QUIT THIS TEST]

# [start uwsgi service]
# uwsgi --ini uwsgi.ini
# [reload uwsgi service]
# uwsgi --reload /tmp/uwsgi_inc.pid
# [stop uwsgi service]
# uwsgi --stop /tmp/uwsgi_inc.pid
# [or not so gracefully: kill -9 `pidof uwsgi`]

# [config nginx and restart]
# cp uwsgi_params /var/www/
# cp nginx.conf /etc/nginx/sites-enabled/default
# service nginx restart
```