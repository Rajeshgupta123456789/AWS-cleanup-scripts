import boto3

def delete_unused_nat_gateways():
    ec2 = boto3.client('ec2')

    nat_gateways = ec2.describe_nat_gateways()['NatGateways']
    for nat in nat_gateways:
        state = nat['State']
        nat_id = nat['NatGatewayId']
        vpc_id = nat['VpcId']

        # Skip if not in 'available' state
        if state != 'available':
            continue

        # Check if it's referenced in any route table
        route_tables = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['RouteTables']
        nat_used = any(
            'NatGatewayId' in route.get('NatGatewayId', '') and route['NatGatewayId'] == nat_id
            for rt in route_tables
            for route in rt.get('Routes', [])
        )

        if not nat_used:
            try:
                ec2.delete_nat_gateway(NatGatewayId=nat_id)
                print(f"Deleted unused NAT Gateway: {nat_id}")
            except Exception as e:
                print(f"Failed to delete NAT Gateway {nat_id}: {str(e)}")

def delete_detached_internet_gateways():
    ec2 = boto3.client('ec2')
    igws = ec2.describe_internet_gateways()['InternetGateways']

    for igw in igws:
        igw_id = igw['InternetGatewayId']
        attachments = igw.get('Attachments', [])

        if not attachments:
            try:
                ec2.delete_internet_gateway(InternetGatewayId=igw_id)
                print(f"Deleted detached Internet Gateway: {igw_id}")
            except Exception as e:
                print(f"Failed to delete IGW {igw_id}: {str(e)}")

if __name__ == "__main__":
    delete_unused_nat_gateways()
    delete_detached_internet_gateways()

