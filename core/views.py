from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request,'index.html')
# views.py
from kafka import KafkaProducer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Adjust if you're using a remote Kafka broker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@csrf_exempt
def send_location(request):
    if request.method == 'POST':
        # Parse the received data from the frontend (GPS data)
        data = json.loads(request.body)
        data['timestamp'] = time.time()  # Add timestamp for reference

        # Send the data to Kafka topic
        producer.send('driver_locations', data)

        # Flush the producer buffer
        producer.flush()

        return JsonResponse({'status': 'sent to Kafka'})
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
