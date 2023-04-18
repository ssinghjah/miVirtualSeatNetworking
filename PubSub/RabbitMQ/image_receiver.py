#!/usr/bin/env python
import pika , ast, sys, os, json, time , pandas as pd

# Here we define the main script that will be executed forever until a keyboard interrupt exception is received
def main():
    credentials = pika.PlainCredentials('admin', 'mivirtual#rabbitls')
    parameters = pika.ConnectionParameters(host='3.90.187.57', port=5672, virtual_host='/', credentials=credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    
    # Since RabbitMQ works asynchronously, every time you receive a message, a callback function is called. We will simply print the message body to the terminal 
    # l1 = []
    def callback(ch, method, properties, body):

        msg = json.loads(body.decode("utf-8"))

        # Payload = body.decode("utf-8")
        Payload = msg["payload"]
        # print()
        Payload = ast.literal_eval(Payload)
        print(type(Payload))
        pt = "C:/Users/DELL/Downloads/RA doc/rabbitmq/" + msg["name"]

        with open(pt, "wb") as f:
            f.write(Payload)

        
        # print("Data Received : {}".format(Payload))
        
        # print(" [x] Received %r" % body)
        # print(body)
        # msg = json.loads(body.decode())
        # msg["receive_timestamp"] = time.time()
        # print(msg)
        # l1.append(msg)
        # pd.DataFrame(l1).to_csv("consumer_data_1ms.csv")
        # print(body["send_timestamp"])

    # Consume a message from a queue. The auto_ack option simplifies our example, as we do not need to send back an acknowledgement query to RabbitMQ which we would normally want in production
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    # Start listening for messages to consume
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)