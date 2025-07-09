import boto3
from datetime import datetime, timezone, timedelta

def check_iam_users():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(days=90)

    for user in users:
        username = user['UserName']
        print(f"\n🔍 Checking user: {username}")

        # MFA check
        mfa = iam.list_mfa_devices(UserName=username)
        if not mfa['MFADevices']:
            print(f"❌ {username} does NOT have MFA enabled.")

        # Access key check
        keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        for key in keys:
            if key['Status'] == 'Active' and key['CreateDate'] < threshold:
                print(f"⚠️ Access key for {username} is older than 90 days (Created: {key['CreateDate']})")

        # Admin privilege check
        attached_policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
        for policy in attached_policies:
            if policy['PolicyName'] == 'AdministratorAccess':
                print(f"⚠️ {username} has AdministratorAccess attached!")

if __name__ == "__main__":
    check_iam_users()

