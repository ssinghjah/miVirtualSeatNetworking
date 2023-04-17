from kafka import KafkaConsumer

consumer = KafkaConsumer( bootstrap_servers='3.90.187.57:9092',
              api_version=(2,0,2))

consumer.subscribe(['Topic_2','Topic_1'])
print("Gonna start listening ['Topic_2','Topic_1']")

while True:
    raw_messages = consumer.poll(
        timeout_ms=100, max_records=200
    )
    for topic_partition, messages in raw_messages.items():
        if topic_partition.topic == 'Topic_2':
            print("Topic_2 ",messages)
        elif topic_partition.topic == 'Topic_1':
            print("Topic_1 ",messages)

