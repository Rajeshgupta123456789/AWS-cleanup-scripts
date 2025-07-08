import boto3

def delete_unused_amis():
    ec2 = boto3.client('ec2')
    account_id = boto3.client('sts').get_caller_identity()['Account']

    # Get all private AMIs
    images = ec2.describe_images(Owners=[account_id])['Images']
    all_ami_ids = {img['ImageId']: img for img in images}

    # Find AMIs in use by EC2 instances
    reservations = ec2.describe_instances()['Reservations']
    used_amis = {instance['ImageId']
                 for r in reservations
                 for instance in r['Instances'] if 'ImageId' in instance}

    # Unused AMIs
    unused_amis = set(all_ami_ids.keys()) - used_amis

    if not unused_amis:
        print("No unused AMIs found.")
        return

    for ami_id in unused_amis:
        try:
            # Delete AMI
            ec2.deregister_image(ImageId=ami_id)
            print(f"Deregistered AMI: {ami_id}")

            # Delete associated snapshots
            for bd in all_ami_ids[ami_id].get('BlockDeviceMappings', []):
                if 'Ebs' in bd and 'SnapshotId' in bd['Ebs']:
                    snap_id = bd['Ebs']['SnapshotId']
                    try:
                        ec2.delete_snapshot(SnapshotId=snap_id)
                        print(f"Deleted associated snapshot: {snap_id}")
                    except Exception as e:
                        print(f"Failed to delete snapshot {snap_id}: {str(e)}")
        except Exception as e:
            print(f"Failed to deregister AMI {ami_id}: {str(e)}")

if __name__ == "__main__":
    delete_unused_amis()

