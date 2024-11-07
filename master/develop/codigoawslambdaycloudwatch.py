import boto3
import time

cloudwatch = boto3.client('cloudwatch')

def record_latency_metric(latency_value):
    cloudwatch.put_metric_data(
        Namespace='MyApp/Performance',
        MetricData=[
            {
                'MetricName': 'API_Latency',
                'Value': latency_value,
                'Unit': 'Milliseconds'
            },
        ]
    )

# Ejemplo de uso de la función de métricas
start_time = time.time()
# Simulación de procesamiento de la API
time.sleep(0.2)  # Latencia simulada
latency = (time.time() - start_time) * 1000
record_latency_metric(latency)
