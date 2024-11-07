import boto3

cloudwatch = boto3.client('cloudwatch')

def set_latency_alert():
    cloudwatch.put_metric_alarm(
        AlarmName='HighAPILatency',
        MetricName='API_Latency',
        Namespace='MyApp/Performance',
        Statistic='Average',
        Threshold=300,
        Period=300,  # Cada 5 minutos
        EvaluationPeriods=1,
        ComparisonOperator='GreaterThanThreshold',
        AlarmActions=['arn:aws:sns:us-east-1:123456789012:NotifyMe']
    )

set_latency_alert()
