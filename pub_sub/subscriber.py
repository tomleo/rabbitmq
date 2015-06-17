#!/usr/bin/env python
import time

import pika

server='owl.rmq.cloudamqp.com'
user = 'orokumby'
vhost = user
password = 'FSNRAv0olz1wb9RUWjGXfr9wjgQDObUp'
exchange = 'logs'


credentials = pika.PlainCredentials(user, password)
params = pika.ConnectionParameters(host=server,
                                   port=5672,
                                   virtual_host=vhost,
                                   credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange=exchange, type='fanout')

# Once we disconnect, the queue should be deleted.
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=exchange, queue=queue_name)

print " [*] Waiting for messages. To exit press CTRL+C"

def callback(ch, method, properties, body):
    print " [x] %r" % (body,)

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()

