#!/usr/bin/env python
import pika,json,pandas as pd,time

credentials = pika.PlainCredentials('admin', 'mivirtual#rabbitls')
parameters = pika.ConnectionParameters(host='3.90.187.57', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

# def callback(ch, method, properties, body):
#     print(" [x] %r" % body)
l1 = []
def callback(ch, method, properties, body):
    # print(" [x] Received %r" % body)
    print(body)
    msg = json.loads(body.decode())
    msg["receive_timestamp"] = time.time()
    print(msg)
    l1.append(msg)
    pd.DataFrame(l1).to_csv("consumer_data.csv")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()