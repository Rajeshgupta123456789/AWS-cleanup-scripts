import boto3

def delete_unused_albs_nlbs():
    elbv2 = boto3.client('elbv2')

    # Get all ALBs and NLBs
    lbs = elbv2.describe_load_balancers()['LoadBalancers']
    if not lbs:
        print("No ALBs/NLBs found.")
        return

    for lb in lbs:
        lb_arn = lb['LoadBalancerArn']
        lb_name = lb['LoadBalancerName']

        # Get associated target groups
        tg_response = elbv2.describe_target_groups(LoadBalancerArn=lb_arn)
        if not tg_response['TargetGroups']:
            try:
                elbv2.delete_load_balancer(LoadBalancerArn=lb_arn)
                print(f"Deleted ALB/NLB with no target groups: {lb_name}")
            except Exception as e:
                print(f"Failed to delete {lb_name}: {str(e)}")

def delete_unused_classic_elbs():
    elb = boto3.client('elb')

    # Get all Classic ELBs
    classic_elbs = elb.describe_load_balancers()['LoadBalancerDescriptions']
    if not classic_elbs:
        print("No Classic ELBs found.")
        return

    for elb_desc in classic_elbs:
        name = elb_desc['LoadBalancerName']
        instances = elb_desc['Instances']
        if not instances:
            try:
                elb.delete_load_balancer(LoadBalancerName=name)
                print(f"Deleted unused Classic ELB: {name}")
            except Exception as e:
                print(f"Failed to delete Classic ELB {name}: {str(e)}")

if __name__ == "__main__":
    delete_unused_albs_nlbs()
    delete_unused_classic_elbs()

