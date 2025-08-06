from confluent_kafka import Consumer
from config import config

topic = "test_topic1"

conf = {
    **config,
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([topic])

print("Consuming messages...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
        else:
            print(f"Received: {msg.value().decode('utf-8')} from partition {msg.partition()}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
