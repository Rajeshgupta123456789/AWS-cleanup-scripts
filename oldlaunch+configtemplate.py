import boto3

def delete_unused_launch_templates():
    ec2 = boto3.client('ec2')
    asg = boto3.client('autoscaling')

    # Get all launch templates
    templates = ec2.describe_launch_templates()['LaunchTemplates']
    used_template_ids = set()

    # Get all ASGs and their launch templates
    asgs = asg.describe_auto_scaling_groups()['AutoScalingGroups']
    for group in asgs:
        if 'LaunchTemplate' in group:
            used_template_ids.add(group['LaunchTemplate']['LaunchTemplateId'])

    for tpl in templates:
        tpl_id = tpl['LaunchTemplateId']
        if tpl_id not in used_template_ids:
            try:
                ec2.delete_launch_template(LaunchTemplateId=tpl_id)
                print(f"Deleted unused Launch Template: {tpl_id}")
            except Exception as e:
                print(f"Failed to delete Launch Template {tpl_id}: {str(e)}")

def delete_unused_launch_configs():
    asg = boto3.client('autoscaling')

    # Get all launch configurations and ASGs
    launch_configs = asg.describe_launch_configurations()['LaunchConfigurations']
    all_config_names = {lc['LaunchConfigurationName'] for lc in launch_configs}

    used_configs = {
        group['LaunchConfigurationName']
        for group in asg.describe_auto_scaling_groups()['AutoScalingGroups']
        if 'LaunchConfigurationName' in group
    }

    unused_configs = all_config_names - used_configs

    for config_name in unused_configs:
        try:
            asg.delete_launch_configuration(LaunchConfigurationName=config_name)
            print(f"Deleted unused Launch Configuration: {config_name}")
        except Exception as e:
            print(f"Failed to delete Launch Configuration {config_name}: {str(e)}")

if __name__ == "__main__":
    delete_unused_launch_templates()
    delete_unused_launch_configs()

