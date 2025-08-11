from confluent_kafka import Producer
from config import COMMON_CONF, TOPIC
import time

producer = Producer(COMMON_CONF)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}", flush=True)
    else:
        print(f"Produced: {msg.value().decode()}", flush=True)

i = 0
try:
    while True:
        message = f"Message {i}"
        producer.produce(TOPIC, value=message.encode(), callback=delivery_report)
        producer.poll(0)
        i += 1
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopping producer...", flush=True)
finally:
    producer.flush()
