from kafka import KafkaConsumer
import pandas as pd
import time

consumer = KafkaConsumer( bootstrap_servers='3.90.187.57:9092',
              api_version=(2,0,2))

consumer.subscribe(['Topic_1','Topic_3'])
print("Gonna start listening ['Topic_1','Topic_3']")

l1 = []
c = 0
while True:
    
    # dict1 = {}
    raw_messages = consumer.poll(
        timeout_ms=5
            )
    # print(time)


    if len(raw_messages.items()) > 0:
        messages = next(iter(raw_messages.values()))[0]
        print(messages)
        # break

    # for topic_partition, messages in raw_messages.items():
        c = c + 1
    #     print(messages[0])
    #     # if topic_partition.topic == 'Topic_1':
    #     #     print("Topic_1 ",messages)
            
    #     # elif topic_partition.topic == 'Topic_3':
    #     #     print("Topic_3 ",messages)
    #     # print(messages[0].topic)
        dict1 = {"timestamp":messages.timestamp,
              "topic":messages.topic,
              "producer_msg":messages.value}
        l1.append(dict1)
        print(dict1)
        print(c)
    if c >= 1:
        break
    # break
# pd.DataFrame(l1).to_csv("100ms_kafka04.csv")


