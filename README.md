# AWS-Threat-Detection-and-Automated-Prevention-Management
Overview
This project demonstrates an automated security monitoring and threat mitigation system using AWS GuardDuty, CloudWatch, Lambda, and SNS. The system detects malicious activities in an AWS environment and automatically isolates compromised instances to prevent further damage.

Features
✔ AWS GuardDuty for real-time threat detection
✔ AWS CloudWatch for event-driven automation
✔ AWS Lambda for automated response and remediation
✔ AWS SNS for alert notifications
✔ EC2 Security Isolation to protect the network

Architecture
The system follows this workflow:
* GuardDuty detects malicious activity (e.g., port scans, unauthorized access).
* CloudWatch Event Rules capture GuardDuty findings.
* SNS Notification is triggered to alert security teams.
* AWS Lambda automatically isolates the compromised EC2 instance by modifying its security group.

Prerequisites
* AWS Account
* IAM permissions for GuardDuty, CloudWatch, Lambda, SNS, and EC2
* Python 3.x
* AWS CLI installed and configured

Setup and Deployment
•	Let’s get started by enabling GuardDuty to capture findings. GuardDuty uses VPC Flow Logs, CloudTrail Logs, and DNS Logs to detect malicious behavior and generate alerts on the GuardDuty console if a possible compromise is detected.
•	Now, we will create three EC2 instances in the VPC’s public subnet. The first EC2 instance is referred to as a compromised instance because it is performing two suspicious activities: (1) conducting a port scan on an internal server and (2) continuously pinging a host that is considered malicious.
•	The second EC2 instance is an web server that has a few ports exposed as API endpoints for other application servers. To secure this server, we need to create a Security Group with inbound rules for the required ports and attach it to the internal server.
•	Next, we need to create a CloudWatch Event Rule that will collect logs from the event source and forward them to the target service for alert notifications and remediation. According to the architecture diagram, the target services will be SNS (Simple Notification Service) and AWS Lambda.
•	To create a CloudWatch Event Rule, we must first create the target service. For SNS, create an SNS Topic named "guardduty-security-topic", followed by creating a subscription. Select Protocol as “Email” and enter an endpoint email address. All alert notifications will be sent to the email address added to the subscription.
•	Navigate to CloudWatch → Events → Rules, and create a new rule named "guardduty-findings-rule". Select Service Name as “GuardDuty” and Event Type as “GuardDuty Findings.” Next, select the targets, which will be triggered when an event match 

the criteria. The first target is SNS, which we created in the previous step. Select SNS Topic and choose "guardduty-security-topic" as the topic name. Then, click Add Target.
•	 At this stage, we have completed one pipeline, i.e., from VPC Flow Logs to SNS. Now, if GuardDuty detects any findings, the subscribers of the "guardduty-security-topic" SNS Topic will receive email notifications.
•	The remaining step is the remediation process, which we will implement using the boto3 framework in AWS Lambda functions.
•	Lambda: The idea behind the remediation is to change the security group of the compromised instance. There are two things which are needed for Lambda:
1.	A security group named “compromised-ec2-sg” with no inbound or outbound rules. This ensures that the affected instance is completely isolated from the environment.
2.	An IAM role named “lambda-guardduty-role” for Lambda, which must have sufficient permissions to modify EC2 security groups. For now, we will grant AmazonEC2FullAccess and AWSLambdaBasicExecutionRole.
•	Steps to Configure AWS Lambda:
1.	Create an AWS Lambda function named “guardduty-pipeline-lambda” with Python 3.8 as the runtime.
2.	In the permissions section, select “Use an existing role” and specify the previously created “lambda-guardduty-role”.
3.	Add a trigger in Lambda: select CloudWatch Events, then choose the rule “guardduty-findings-rule” that we created earlier.
•	Now, the Lambda trigger is successfully configured. You can verify this in CloudWatch Events Rules under “guardduty-

•	findings-rule”, where the target lists should now include both the Lambda function and the SNS topic.
•	Now we will write a snippet for which we will be using boto3 for accessing AWS resources. The code below, snippet represents if finding Recon:EC2/Portscan is detected (reproduction discussed in Attack section) then the victim machine’s security group will be changed to “compromised-ec2-sg” and in our case, it’s the first EC2 i.e. compromised instance. We are isolating the instance from every other resource. This is just to make sure there are no backdoor connections that exist on the compromised instance.
