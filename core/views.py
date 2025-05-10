from django.shortcuts import render
from kafka import KafkaProducer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

# Optional: Keep a global reference to reuse the producer
_kafka_producer = None
def get_kafka_producer():
    global _kafka_producer
    if _kafka_producer is None:
        try:
            _kafka_producer = KafkaProducer(
                bootstrap_servers='kafka:9092',  # Use the Docker service name
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=5,
                retry_backoff_ms=1000
            )
        except Exception as e:
            print(f"Error initializing KafkaProducer: {e}")
            return None
    return _kafka_producer


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def send_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['timestamp'] = time.time()

        producer = get_kafka_producer()
        if not producer:
            return JsonResponse({'error': 'Kafka not available'}, status=500)

        try:
            producer.send('driver_locations', data)
            producer.flush()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'status': 'sent to Kafka'})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)
