from kafka import KafkaConsumer
import json
import threading
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def start_kafka_consumer():
    consumer = KafkaConsumer(
        'driver_locations',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    channel_layer = get_channel_layer()

    for message in consumer:
        async_to_sync(channel_layer.group_send)(
            "locations",
            {
                "type": "send_location",
                "data": message.value
            }
        )

def start_consumer_thread():
    thread = threading.Thread(target=start_kafka_consumer)
    thread.daemon = True
    thread.start()
