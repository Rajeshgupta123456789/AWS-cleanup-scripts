import boto3

def release_unassociated_eips():
    ec2 = boto3.client('ec2')

    addresses = ec2.describe_addresses()['Addresses']
    unassociated_eips = [addr for addr in addresses if 'InstanceId' not in addr and 'NetworkInterfaceId' not in addr]

    if not unassociated_eips:
        print("No unassociated Elastic IPs found.")
        return

    for eip in unassociated_eips:
        try:
            ec2.release_address(AllocationId=eip['AllocationId'])
            print(f"Released Elastic IP: {eip.get('PublicIp')}")
        except Exception as e:
            print(f"Failed to release EIP {eip.get('PublicIp')}: {str(e)}")

if __name__ == "__main__":
    release_unassociated_eips()

