#!/usr/bin/env python
import pika


credentials = pika.PlainCredentials('orokumby', 'FSNRAv0olz1wb9RUWjGXfr9wjgQDObUp')

params = pika.ConnectionParameters(host='owl.rmq.cloudamqp.com',
                                   port=5672,
                                   virtual_host='orokumby',
                                   credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hello')

print " [*] Waiting for messages. To exit press CTRL+C"

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(callback, queue='hello', no_ack=True)
channel.start_consuming()
