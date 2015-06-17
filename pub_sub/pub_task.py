#!/usr/bin/env python
import sys
import pika

server = 'owl.rmq.cloudamqp.com'
vhost = 'orokumby'
user = 'orokumby'
password = 'FSNRAv0olz1wb9RUWjGXfr9wjgQDObUp'
exchange='logs'

# Giving a queue a name is important when you want point multiple workers at
# the same queue.

credentials = pika.PlainCredentials(user, password)
params = pika.ConnectionParameters(host=server,
                                   port=5672,
                                   virtual_host=vhost,
                                   credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='logs', type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange=exchange,
                      routing_key='',
                      body=message)

print " [x] Sent %r" % (message,)
connection.close()
