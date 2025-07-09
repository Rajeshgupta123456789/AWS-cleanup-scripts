import boto3
import csv

def get_regions():
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions()['Regions']
    return [region['RegionName'] for region in regions]

def find_open_ssh_security_groups(region):
    ec2 = boto3.client('ec2', region_name=region)
    vulnerable_sgs = []

    try:
        response = ec2.describe_security_groups()
        for sg in response['SecurityGroups']:
            for perm in sg.get('IpPermissions', []):
                if perm.get('FromPort') == 22 and perm.get('ToPort') == 22 and perm.get('IpProtocol') == 'tcp':
                    for ip_range in perm.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            vulnerable_sgs.append((region, sg['GroupName'], sg['GroupId'], 'IPv4'))
                    for ip_range in perm.get('Ipv6Ranges', []):
                        if ip_range.get('CidrIpv6') == '::/0':
                            vulnerable_sgs.append((region, sg['GroupName'], sg['GroupId'], 'IPv6'))
    except Exception as e:
        print(f"Error in {region}: {str(e)}")

    return vulnerable_sgs

def main():
    regions = get_regions()
    all_vulnerable = []

    for region in regions:
        print(f"Scanning region: {region}")
        sg_list = find_open_ssh_security_groups(region)
        all_vulnerable.extend(sg_list)

    if not all_vulnerable:
        print("✅ No security groups with SSH open to the world found.")
        return

    with open('open_ssh_sgs.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Region', 'Group Name', 'Group ID', 'IP Version'])
        writer.writerows(all_vulnerable)

    print(f"⚠️ Found {len(all_vulnerable)} security groups with port 22 open to the world.")
    print("📄 Results saved to: open_ssh_sgs.csv")

if __name__ == "__main__":
    main()

