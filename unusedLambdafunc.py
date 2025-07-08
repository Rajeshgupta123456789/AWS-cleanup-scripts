import boto3
from datetime import datetime, timedelta, timezone

def delete_unused_lambda_functions(days_unused=30):
    lambda_client = boto3.client('lambda')
    cw = boto3.client('cloudwatch')

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=days_unused)

    paginator = lambda_client.get_paginator('list_functions')

    for page in paginator.paginate():
        for fn in page['Functions']:
            fn_name = fn['FunctionName']

            # Skip functions tagged Keep=True
            try:
                tags = lambda_client.list_tags(Resource=fn['FunctionArn']).get('Tags', {})
                if tags.get('Keep', '').lower() == 'true':
                    continue
            except Exception as e:
                print(f"Error getting tags for {fn_name}: {str(e)}")

            try:
                metrics = cw.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Invocations',
                    Dimensions=[{'Name': 'FunctionName', 'Value': fn_name}],
                    StartTime=start_time,
                    EndTime=now,
                    Period=86400,
                    Statistics=['Sum']
                )

                if not metrics['Datapoints']:
                    lambda_client.delete_function(FunctionName=fn_name)
                    print(f"Deleted unused Lambda function: {fn_name}")
            except Exception as e:
                print(f"Error processing Lambda {fn_name}: {str(e)}")

if __name__ == "__main__":
    delete_unused_lambda_functions()

