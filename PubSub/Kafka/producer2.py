import json
import time

from kafka import KafkaProducer

ORDER_LIMIT = 1500

producer = KafkaProducer(
              api_version=(2,0,2))

print("Going to be generating order after 10 seconds")
print("Will generate one unique order every 5 seconds")

# time.sleep(10)

for i in range(ORDER_LIMIT):
    i = str(i) + " producer 2"
    data = {
        "order_id": i
    }

    producer.send("Topic_2", json.dumps(data).encode("utf-8"))
    producer.send("Topic_3", json.dumps(data).encode("utf-8"))
    producer.flush()
    print(f"Done Sending..{i}")
    # time.sleep(5)
