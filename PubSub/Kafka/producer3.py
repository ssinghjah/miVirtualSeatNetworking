import json
import time

from kafka import KafkaProducer

ORDER_LIMIT = 7100

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
              api_version=(2,0,2))

print("Going to be generating order after 10 seconds")
print("Will generate one unique order every 5 seconds")

# time.sleep(10)

for i in range(ORDER_LIMIT):
    i = str(i) + " producer 3"
    data = {
        "order_id": i
    }

    # producer.send("Topic_3", json.dumps(data).encode("utf-8"))
    producer.send("Topic_1", json.dumps(data).encode("utf-8"))
    producer.flush()
    print(f"Done Sending..{i}")
    # break
    # time.sleep(5)
