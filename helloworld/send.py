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
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()
