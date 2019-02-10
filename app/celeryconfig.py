# Broker settings.
broker_url = 'redis://redis-q:6379'

# List of modules to import when the Celery worker starts.
imports = ('app.tasks',)

# Using the redis to store task state and results.
result_backend = 'redis://redis-q:6379'

task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# Users and groups
uid = 'celery'
gid = 'celery'
