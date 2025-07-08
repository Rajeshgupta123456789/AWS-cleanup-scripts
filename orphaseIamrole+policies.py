import boto3

def delete_unused_iam_roles():
    iam = boto3.client('iam')

    roles = iam.list_roles()['Roles']

    for role in roles:
        role_name = role['RoleName']
        role_path = role['Path']

        # Skip service-linked or AWS-managed roles
        if role_path.startswith('/aws-service-role/') or role_name.startswith('AWSServiceRoleFor'):
            continue

        # Skip roles with Keep=True tag
        try:
            tags = iam.list_role_tags(RoleName=role_name).get('Tags', [])
            tag_dict = {tag['Key']: tag['Value'] for tag in tags}
            if tag_dict.get('Keep', '').lower() == 'true':
                continue
        except Exception:
            pass  # Some roles may not have tags

        try:
            # Check instance profile attachment
            profiles = iam.list_instance_profiles_for_role(RoleName=role_name)['InstanceProfiles']
            if profiles:
                continue  # Role still in use

            # Detach managed policies
            attached_policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
            for policy in attached_policies:
                iam.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])

            # Delete inline policies
            inline_policies = iam.list_role_policies(RoleName=role_name)['PolicyNames']
            for policy_name in inline_policies:
                iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)

            # Delete the role
            iam.delete_role(RoleName=role_name)
            print(f"Deleted unused IAM Role: {role_name}")
        except Exception as e:
            print(f"Failed to delete IAM Role {role_name}: {str(e)}")

if __name__ == "__main__":
    delete_unused_iam_roles()

