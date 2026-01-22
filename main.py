import boto3
import logging
import argparse
import sys
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_ec2_resource(region: str):
    try:
        return boto3.resource("ec2", region_name=region)
    except Exception as e:
        logger.critical(f"AWS connection failed: {e}")
        sys.exit(1)

def manage_instances(ec2, action: str, tag_key: str, tag_value: str):
    logger.info(f"Searching for instances with tag {tag_key}={tag_value}...")
    
    filters = [{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
    instances = ec2.instances.filter(Filters=filters)

    if not list(instances): 
        logger.warning("No instances found matching the criteria.")
        return

    logger.info(f"Found instances. Executing action: {action.upper()}...")

    try:
        if action == 'stop':
            instances.stop()
            logger.info("Stop signal sent to all matching instances successfully.")
            
        elif action == 'start':
            instances.start()
            logger.info("Start signal sent to all matching instances successfully.")
            
    except ClientError as e:
        logger.error(f"AWS Operation Failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS EC2 Batch Power Manager")
    parser.add_argument("--region", default="us-east-1", help="AWS Region (default: us-east-1)")
    parser.add_argument("--env", default="Dev", help="Environment Tag Value (default: Dev)")
    parser.add_argument("--action", choices=["start", "stop"], required=True, help="Action to perform")
    
    args = parser.parse_args()

    ec2_resource = get_ec2_resource(args.region)
    
    manage_instances(
        ec2=ec2_resource, 
        action=args.action, 
        tag_key="Environment", 
        tag_value=args.env
    )
