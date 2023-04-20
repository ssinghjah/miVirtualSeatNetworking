#!/usr/bin/env python
import pika,time,json
import sys

credentials = pika.PlainCredentials(username='admin', password='mivirtual#rabbitls', erase_on_connect=True)
parameters = pika.ConnectionParameters(host='3.90.187.57', port=5672, virtual_host='/', credentials=credentials)

# We are using BlockingConnection adapter to start a session. It uses a procedural approach to using Pika and has most of the asynchronous expectations removed
connection = pika.BlockingConnection(parameters)
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

for i in range(1,101):
    message = {"order_id":i,"send_timestamp":time.time()}
    channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))
    print(" [x] Sent %r" % message)
connection.close()