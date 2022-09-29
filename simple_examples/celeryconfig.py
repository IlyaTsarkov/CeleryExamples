REDIS_HOST = 'redis://localhost'
REDIS_PORT = '6379'
REDIS_BD = '0'

broker_url = REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_BD
# broker_url = 'amqp://myuser:mypassword@localhost:5672/example_host'
result_backend = REDIS_HOST

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Moscow'
enable_utc = True

