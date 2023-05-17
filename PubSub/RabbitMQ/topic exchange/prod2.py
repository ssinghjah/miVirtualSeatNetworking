#publisher.py
import pika


credentials = pika.PlainCredentials(username='admin', password='mivirtual#rabbitls', erase_on_connect=True)
parameters = pika.ConnectionParameters(host='35.171.54.199', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters) 
channel = connection.channel()
channel.exchange_declare(exchange='log1',
exchange_type='topic')
routing_key = 'delhi.azhar'
message = routing_key
channel.basic_publish(exchange='log1',routing_key=routing_key, body=message)

print("[x] Sent message %r for %r" % (message,routing_key))

