import boto3
import logging
import botocore.exceptions
from typing import List, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

AWS_REGION = "us-east-1"

TAG_FILTERS = [
    {
        "Name": "tag:Environment",
        "Values": ["Dev"]
    }
]

def get_target_instances(ec2_resource: Any) -> List[Any]:
    logger.info("Scanning EC2 instances with defined tag filters...")
    try:
        instances = list(ec2_resource.instances.filter(Filters=TAG_FILTERS))
        logger.info(f"{len(instances)} matching EC2 instances found.")
        return instances
    except botocore.exceptions.ClientError as e:
        logger.error(f"AWS API error while fetching instances: {e}")
        return []

def stop_instances(instances: List[Any]) -> None:
    if not instances:
        logger.warning("No instances provided for stop operation.")
        return

    for instance in instances:
        instance_id = instance.id
        try:
            instance.reload()
            current_state = instance.state["Name"]

            logger.info(f"Instance {instance_id} current state: {current_state}")

            if current_state == "running":
                logger.info(f"Stopping instance: {instance_id}")
                instance.stop()
                instance.wait_until_stopped()
                logger.info(f"Instance successfully stopped: {instance_id}")

            elif current_state == "stopped":
                logger.info(f"Instance already stopped, skipping: {instance_id}")

        except botocore.exceptions.ClientError as e:
            logger.error(f"Error while stopping instance {instance_id}: {e}")

def start_instances(instances: List[Any]) -> None:
    if not instances:
        logger.warning("No instances provided for start operation.")
        return

    for instance in instances:
        instance_id = instance.id
        try:
            instance.reload()
            current_state = instance.state["Name"]

            logger.info(f"Instance {instance_id} current state: {current_state}")

            if current_state == "stopped":
                logger.info(f"Starting instance: {instance_id}")
                instance.start()
                instance.wait_until_running()
                logger.info(f"Instance successfully running: {instance_id}")

            elif current_state == "running":
                logger.info(f"Instance already running, skipping: {instance_id}")

        except botocore.exceptions.ClientError as e:
            logger.error(f"Error while starting instance {instance_id}: {e}")

if __name__ == "__main__":
    try:
        ec2 = boto3.resource("ec2", region_name=AWS_REGION)

        target_instances = get_target_instances(ec2)

        if target_instances:
            logger.info("Operation menu loaded.")
            logger.info("1: Stop instances (End of business hours)")
            logger.info("2: Start instances (Beginning of business hours)")

            choice = input("Select operation (1/2): ").strip()

            if choice == "1":
                stop_instances(target_instances)
            elif choice == "2":
                start_instances(target_instances)
            else:
                logger.warning("Invalid selection. Operation aborted.")
        else:
            logger.info("No matching instances found. No operation executed.")

    except Exception as main_err:
        logger.critical(f"Fatal application error: {main_err}")
