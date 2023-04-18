#!/usr/bin/env python
import pika
import time
import json
import pandas as pd
    
import os
from os import listdir


FPS = 30

class Image(object):

    __slots__ = ["filename"]

    def __init__(self, filename):
        self.filename = filename

    @property
    def get(self):
        with open(self.filename, "rb") as f:
            data = f.read()
        return data

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

folder_dir = "C:/Users/DELL/Downloads/RA doc/rabbitmq/ConferenceRoom/"
for images in os.listdir(folder_dir):
    # time.sleep(1/FPS)
    # print(images)
    pt = folder_dir+images
    print(pt)
    # print(type(images))
    img = Image(pt)
    data = img.get
 
    # check if the image ends with png
    # if (images.endswith(".png")):
    #     print(images.get)
    #     break
    # break

# for i in range(5000):
#     time.sleep(0.001)
#     msg = {"send_timestamp":time.time(),"order_id":i}
    msg = {"name":images,"payload":str(data) ,"send_timestamp":time.time()}
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(msg))
    # break
#     l1.append(msg)
# pd.DataFrame(l1).to_csv("producer_data_1ms.csv")
# print("task completed")
# Safely disconnect from RabbitMQ
connection.close()

 
# get the path/directory
# folder_dir = "C:/Users/DELL/Downloads/RA doc/rabbitmq/ConferenceRoom"
# for images in os.listdir(folder_dir):
 
#     # check if the image ends with png
#     if (images.endswith(".png")):
#         print(images)

# def get(self):
#         with open(self.filename, "rb") as f:
#             data = f.read()
#         return data
# image = Image(filename="/Users/soumilshah/Documents/Intelliji/2.png")
#     data = image.get

#     with RabbitMq(server) as rabbitmq:
#         rabbitmq.publish(payload=data)
