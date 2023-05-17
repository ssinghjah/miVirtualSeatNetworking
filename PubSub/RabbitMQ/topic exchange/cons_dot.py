#subscriber.py
import pika,json,time
import sys
credentials = pika.PlainCredentials('admin', 'mivirtual#rabbitls')
parameters = pika.ConnectionParameters(host='35.171.54.199', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='log1',exchange_type='topic')
channel.queue_declare(queue='')
channel.queue_bind(queue='',exchange='log1',routing_key='delhi.')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(body)

channel.basic_consume(
    queue='', on_message_callback=callback, auto_ack=True)

channel.start_consuming()