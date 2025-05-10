from kafka import KafkaConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import threading
import json

def start_kafka_consumer():
    consumer = KafkaConsumer(
        'driver_locations',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    channel_layer = get_channel_layer()

    for message in consumer:
        data = message.value
        driver_id = data.get("driver_id")
        if not driver_id:
            continue

        async_to_sync(channel_layer.group_send)(
            f"location_{driver_id}",
            {
                "type": "send_location",
                "data": data
            }
        )

def start_consumer_thread():
    thread = threading.Thread(target=start_kafka_consumer)
    thread.daemon = True
    thread.start()
