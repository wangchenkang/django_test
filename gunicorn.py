import multiprocessing

preload_app = True
timeout = 300
bind = "127.0.0.1:60012"
pythonpath = "/opt/app/hunting_tracker/"
django_settings = 'web.settings'
work_class = 'gevent'
workers = 1

loglevel = 'debug'
accesslog = '/var/log/gunicorn/hunting_tracker/gunicorn_access.log'
errorlog = '/var/log/gunicorn/hunting_tracker/gunicorn_error.log'
