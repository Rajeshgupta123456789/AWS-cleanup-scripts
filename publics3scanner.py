import boto3

def is_bucket_public(bucket_name, s3_client):
    try:
        # Check bucket ACL
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and ('AllUsers' in grant['Grantee']['URI'] or 'AuthenticatedUsers' in grant['Grantee']['URI']):
                return True, "ACL"

        # Check bucket policy
        try:
            policy = s3_client.get_bucket_policy(Bucket=bucket_name)
            if '"Effect":"Allow"' in policy['Policy'] and ('"Principal":"*"' in policy['Policy'] or '"Principal": "*"' in policy['Policy']):
                return True, "Policy"
        except s3_client.exceptions.NoSuchBucketPolicy:
            pass

    except Exception as e:
        print(f"Error checking {bucket_name}: {e}")
    return False, ""

def scan_public_buckets():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    print("🔎 Scanning for public S3 buckets...\n")

    for bucket in buckets:
        name = bucket['Name']
        is_public, method = is_bucket_public(name, s3)
        if is_public:
            print(f"❌ {name} is public via {method}")
        else:
            print(f"✅ {name} is private")

if __name__ == "__main__":
    scan_public_buckets()

