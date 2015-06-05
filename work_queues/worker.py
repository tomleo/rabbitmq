#!/usr/bin/env python
import time

import pika

server='owl.rmq.cloudamqp.com'
user = 'orokumby'
vhost = user
password = 'FSNRAv0olz1wb9RUWjGXfr9wjgQDObUp'
queue = 'task_queue'


credentials = pika.PlainCredentials(user, password)
params = pika.ConnectionParameters(host=server,
                                   port=5672,
                                   virtual_host=vhost,
                                   credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue, durable=True)

print " [*] Waiting for messages. To exit press CTRL+C"

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(body.count('.'))
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1) # 1 task per worker
channel.basic_consume(callback, queue=queue)
channel.start_consuming()

