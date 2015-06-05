#!/usr/bin/env python
import sys
import pika

server = 'owl.rmq.cloudamqp.com'
vhost = 'orokumby'
user = 'orokumby'
password = 'FSNRAv0olz1wb9RUWjGXfr9wjgQDObUp'
queue = 'task_queue'

credentials = pika.PlainCredentials(user, password)
params = pika.ConnectionParameters(host=server,
                                   port=5672,
                                   virtual_host=vhost,
                                   credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
# RabbitMQ doesn't allow you to redefine an existing queue with different
# parameters and will return an error to any program that tries to do that
channel.queue_declare(queue=queue, durable=True)
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key=queue,
                      body=message,
                      properties=pika.BasicProperties(
                        delivery_mode = 2, # make message persistent    
                      ))
# declaring durable=True will tell RabbitMQ to save messages to disk
# there is still a short time window when RabbitMQ has accepted a message and
# hasn't saved it yet. Also, RabbitMQ doesn't do fsync(2) for every message --
# it may be just saved to cache and not really written to the disk. The
# persistence guarantees aren't strong, but it's more than enough for our
# simple task queue. If you need a stronger guarantee then you can use
# publisher confirms.
print " [x] Sent %r" % (message,)
connection.close()
