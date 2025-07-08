import boto3
from datetime import datetime, timezone, timedelta

def delete_idle_log_groups(days_idle=7):
    logs = boto3.client('logs')
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_idle)

    paginator = logs.get_paginator('describe_log_groups')
    for page in paginator.paginate():
        for group in page['logGroups']:
            log_group_name = group['logGroupName']

            # Skip if tagged Keep=True
            tags = logs.list_tags_log_group(logGroupName=log_group_name).get('tags', {})
            if tags.get('Keep', '').lower() == 'true':
                continue

            # Skip if no metric data (never used)
            if 'storedBytes' not in group or group['storedBytes'] == 0:
                try:
                    logs.delete_log_group(logGroupName=log_group_name)
                    print(f"Deleted unused log group (never used): {log_group_name}")
                    continue
                except Exception as e:
                    print(f"Error deleting {log_group_name}: {str(e)}")

            # Check log stream activity
            streams = logs.describe_log_streams(
                logGroupName=log_group_name,
                orderBy='LastEventTime',
                descending=True,
                limit=1
            ).get('logStreams', [])

            if not streams or streams[0].get('lastEventTimestamp', 0) / 1000 < cutoff.timestamp():
                try:
                    logs.delete_log_group(logGroupName=log_group_name)
                    print(f"Deleted idle log group: {log_group_name}")
                except Exception as e:
                    print(f"Error deleting {log_group_name}: {str(e)}")

if __name__ == "__main__":
    delete_idle_log_groups(days_idle=7)

