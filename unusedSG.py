import boto3

def delete_unused_security_groups():
    ec2 = boto3.client('ec2')

    # Get all security groups
    all_sgs = ec2.describe_security_groups()['SecurityGroups']
    all_sg_ids = {sg['GroupId'] for sg in all_sgs if sg['GroupName'] != 'default'}

    # Get all ENIs (Elastic Network Interfaces) and attached SGs
    enis = ec2.describe_network_interfaces()['NetworkInterfaces']
    used_sg_ids = {sg['GroupId'] for eni in enis for sg in eni['Groups']}

    # Get in-use SGs from EC2 instances
    reservations = ec2.describe_instances()['Reservations']
    for reservation in reservations:
        for instance in reservation['Instances']:
            for sg in instance.get('SecurityGroups', []):
                used_sg_ids.add(sg['GroupId'])

    # Identify unused SGs
    unused_sgs = all_sg_ids - used_sg_ids

    if not unused_sgs:
        print("No unused Security Groups found.")
        return

    for sg_id in unused_sgs:
        try:
            ec2.delete_security_group(GroupId=sg_id)
            print(f"Deleted unused Security Group: {sg_id}")
        except Exception as e:
            print(f"Failed to delete {sg_id}: {str(e)}")

if __name__ == "__main__":
    delete_unused_security_groups()

