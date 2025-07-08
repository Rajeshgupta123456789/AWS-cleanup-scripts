import boto3

def delete_empty_s3_buckets():
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    buckets = s3.list_buckets()['Buckets']

    for bucket in buckets:
        bucket_name = bucket['Name']

        # Skip based on naming pattern (optional safety)
        if any(x in bucket_name for x in ['aws-', 'cloudtrail', 'config', 'log', 'backup']):
            continue

        # Check tags for "Keep"
        try:
            tagging = s3.get_bucket_tagging(Bucket=bucket_name)
            tags = {tag['Key']: tag['Value'] for tag in tagging.get('TagSet', [])}
            if tags.get('Keep', '').lower() == 'true':
                continue
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchTagSet':
                print(f"Error checking tags on {bucket_name}: {str(e)}")

        # Check if bucket is empty
        try:
            objects = list(s3_resource.Bucket(bucket_name).objects.limit(1))
            if not objects:
                s3.delete_bucket(Bucket=bucket_name)
                print(f"Deleted empty S3 bucket: {bucket_name}")
        except Exception as e:
            print(f"Failed to check/delete bucket {bucket_name}: {str(e)}")

if __name__ == "__main__":
    delete_empty_s3_buckets()

