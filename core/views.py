from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
import json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def home(request):
    return render(request, 'home.html')

def track_driver(request, driver_id):
    return render(request, 'map.html', {'driver_id': driver_id})

@csrf_exempt
def send_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['timestamp'] = time.time()
        producer.send('driver_locations', data)
        producer.flush()
        return JsonResponse({'status': 'sent to Kafka'})
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
