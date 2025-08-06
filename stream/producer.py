import time
from confluent_kafka import Producer
from config import config  # config should include Confluent Cloud details

topic = "test_topic1"

producer = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

i = 0
try:
    while True:
        message = f"test-message-{i}"
        producer.produce(topic, message.encode("utf-8"), callback=delivery_report)
        producer.poll(0)  # triggers delivery callbacks
        time.sleep(1)  # sends 1 message per second
        i += 1
except KeyboardInterrupt:
    print("Stopping producer...")
finally:
    producer.flush()
