from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    location = {
        'driver_id': 'driver_1',
        'latitude': 27.7172 + random.uniform(-0.01, 0.01),
        'longitude': 85.3240 + random.uniform(-0.01, 0.01),
        'timestamp': time.time()
    }
    producer.send('driver_locations', location)
    time.sleep(2)
