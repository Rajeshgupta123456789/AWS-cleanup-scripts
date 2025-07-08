import boto3

def delete_stopped_rds_instances():
    rds = boto3.client('rds')

    dbs = rds.describe_db_instances()['DBInstances']
    for db in dbs:
        db_id = db['DBInstanceIdentifier']
        db_status = db['DBInstanceStatus']

        # Skip anything not in 'stopped' state
        if db_status != 'stopped':
            continue

        # Skip if tagged with Keep=True
        try:
            tags = rds.list_tags_for_resource(ResourceName=db['DBInstanceArn'])['TagList']
            tag_dict = {tag['Key']: tag['Value'] for tag in tags}
            if tag_dict.get('Keep', '').lower() == 'true':
                continue
        except Exception as e:
            print(f"Could not fetch tags for {db_id}: {str(e)}")

        try:
            # Terminate without final snapshot
            rds.delete_db_instance(
                DBInstanceIdentifier=db_id,
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True
            )
            print(f"Deleted stopped RDS instance: {db_id}")
        except Exception as e:
            print(f"Failed to delete RDS {db_id}: {str(e)}")

if __name__ == "__main__":
    delete_stopped_rds_instances()

