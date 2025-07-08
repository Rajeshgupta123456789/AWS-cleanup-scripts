import boto3
from datetime import datetime, timezone, timedelta

def delete_old_snapshots(days_old=7):
    ec2 = boto3.client('ec2')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)

    # Get all snapshots owned by the account
    snapshots = ec2.describe_snapshots(OwnerIds=[account_id])['Snapshots']

    for snap in snapshots:
        snapshot_id = snap['SnapshotId']
        start_time = snap['StartTime']

        # Check if it has a "Keep=True" tag
        tags = {t['Key']: t['Value'] for t in snap.get('Tags', [])}
        if tags.get('Keep', '').lower() == 'true':
            continue

        # Only delete if older than threshold
        if start_time < cutoff_date:
            try:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted old snapshot: {snapshot_id}")
            except Exception as e:
                print(f"Failed to delete {snapshot_id}: {str(e)}")

if __name__ == "__main__":
    delete_old_snapshots(days_old=7)  # Change the number of days if needed

