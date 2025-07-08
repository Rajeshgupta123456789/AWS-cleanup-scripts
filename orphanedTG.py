import boto3

def delete_unused_target_groups():
    elbv2 = boto3.client('elbv2')

    # Get all target groups
    target_groups = elbv2.describe_target_groups()['TargetGroups']

    for tg in target_groups:
        tg_arn = tg['TargetGroupArn']
        tg_name = tg['TargetGroupName']

        # Check if the target group is attached to any Load Balancer
        try:
            lb_arns = elbv2.describe_target_groups(TargetGroupArns=[tg_arn])['TargetGroups'][0].get('LoadBalancerArns', [])
            if not lb_arns:
                elbv2.delete_target_group(TargetGroupArn=tg_arn)
                print(f"Deleted unused Target Group: {tg_name}")
        except Exception as e:
            print(f"Failed to delete Target Group {tg_name}: {str(e)}")

if __name__ == "__main__":
    delete_unused_target_groups()

