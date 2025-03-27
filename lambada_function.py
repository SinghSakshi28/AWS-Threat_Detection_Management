import boto3
ec2 = boto3.resource('ec2')
isolated_sg = 'sg-06e411d1ae8b4df01' # ID of Security group “compromised-ec2-sg”

def lambda_handler(event, context):
 """Method to change the security group of the affected EC2 instance
 """
 print(event)
 finding_type = event['detail']['type']
 instance_id = event['detail']['resource']['instanceDetails']['instanceId']

 # logging the finding and instance details 
 print(f"Finding type: {finding_type}")
 print(f"Instance ID: {instance_id}")

 if finding_type == 'Recon:EC2/Portscan':
  victim_ec2 = ec2.Instance(instance_id)
 # If any suspicious activity is detected by GuardDuty, then the affected ec2 will be moved to this security group
 victim_ec2.modify_attribute(Groups=[isolated_sg])
