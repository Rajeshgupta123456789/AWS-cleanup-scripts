import boto3

def terminate_stopped_instances():
    ec2 = boto3.client('ec2')

    # Get all instances that are stopped
    response = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['stopped']}
    ])

    stopped_instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]

    if not stopped_instance_ids:
        print("No stopped EC2 instances found.")
        return

    for instance_id in stopped_instance_ids:
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
            print(f"Terminated EC2 instance: {instance_id}")
        except Exception as e:
            print(f"Failed to terminate {instance_id}: {str(e)}")

if __name__ == "__main__":
    terminate_stopped_instances()

