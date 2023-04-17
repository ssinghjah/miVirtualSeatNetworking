#!/usr/bin/env python
import pika
import time
import json
import pandas as pd
# If you want to have a more secure SSL authentication, use ExternalCredentials object instead
credentials = pika.PlainCredentials(username='admin', password='mivirtual#rabbitls', erase_on_connect=True)
parameters = pika.ConnectionParameters(host='3.90.187.57', port=5672, virtual_host='/', credentials=credentials)

# We are using BlockingConnection adapter to start a session. It uses a procedural approach to using Pika and has most of the asynchronous expectations removed
connection = pika.BlockingConnection(parameters)
# A channel provides a wrapper for interacting with RabbitMQ
channel = connection.channel()

# Check for a queue and create it, if necessary
channel.queue_declare(queue='hello')
l1 = []
# For the sake of simplicity, we are not declaring an exchange, so the subsequent publish call will be sent to a Default exchange that is predeclared by the broker
for i in range(5000):
    time.sleep(0.001)
    msg = {"send_timestamp":time.time(),"order_id":i}
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(msg))
    l1.append(msg)
pd.DataFrame(l1).to_csv("producer_data_1ms.csv")
print("task completed")
# Safely disconnect from RabbitMQ
connection.close()