import boto3
from datetime import datetime, timezone, timedelta

def delete_old_secrets(days_old=30):
    secretsmanager = boto3.client('secretsmanager')
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days_old)

    paginator = secretsmanager.get_paginator('list_secrets')

    for page in paginator.paginate():
        for secret in page['SecretList']:
            secret_name = secret['Name']
            last_changed = secret.get('LastChangedDate', None)
            tags = {tag['Key']: tag['Value'] for tag in secret.get('Tags', [])}

            if tags.get('Keep', '').lower() == 'true':
                continue

            # If never changed, skip
            if not last_changed:
                continue

            if last_changed < cutoff:
                try:
                    secretsmanager.delete_secret(
                        SecretId=secret['ARN'],
                        ForceDeleteWithoutRecovery=True  # use recovery if needed
                    )
                    print(f"Deleted old secret: {secret_name}")
                except Exception as e:
                    print(f"Failed to delete secret {secret_name}: {str(e)}")

if __name__ == "__main__":
    delete_old_secrets(days_old=30)

