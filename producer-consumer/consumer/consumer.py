from confluent_kafka import Consumer
from config import COMMON_CONF, TOPIC, GROUP_ID
import signal

running = True

def signal_handler(sig, frame):
    global running
    print("\nStopping consumer...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

conf = COMMON_CONF.copy()
conf.update({
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
})

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

print("Consumer started. Waiting for messages...", flush=True)

try:
    while running:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}", flush=True)
            continue
        print(f"Consumed: {msg.value().decode('utf-8')}", flush=True)
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    consumer.close()
    print("Consumer closed.")
