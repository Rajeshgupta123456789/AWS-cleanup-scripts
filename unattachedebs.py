import boto3

def delete_unattached_ebs_volumes():
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

    if not volumes['Volumes']:
        print("No unattached EBS volumes found.")
        return

    for vol in volumes['Volumes']:
        vol_id = vol['VolumeId']
        try:
            ec2.delete_volume(VolumeId=vol_id)
            print(f"Deleted EBS Volume: {vol_id}")
        except Exception as e:
            print(f"Failed to delete {vol_id}: {str(e)}")

if __name__ == "__main__":
    delete_unattached_ebs_volumes()

