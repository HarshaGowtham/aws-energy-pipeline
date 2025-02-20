import os
import json
import boto3
import decimal
from datetime import datetime

# Initialize AWS clients
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
sns_client = boto3.client("sns")

# Use environment variable for DynamoDB table
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):
    """Triggered when a new file is uploaded to S3."""
    
    # Get bucket name and file key from S3 event
    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]

        print(f"Processing file: s3://{bucket_name}/{object_key}")

        # Download file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8")
        energy_data = json.loads(file_content)

        # Process each record
        table = dynamodb.Table(DYNAMODB_TABLE)
        for entry in energy_data:
            print("Received entry:", entry)

            site_id = entry.get("site_id")
            record_timestamp = str(entry.get("timestamp", ""))  # Ensure timestamp is always a string

            # Debugging: Check which field is missing
            if not site_id or not record_timestamp:
                print(f" MISSING FIELD - site_id: {site_id}, record_timestamp: {record_timestamp}")
                print(f" Skipping entry due to missing keys: {entry}")
                continue

            # Convert energy values to Decimal
            energy_generated = decimal.Decimal(str(entry.get("energy_generated_kwh", 0)))
            energy_consumed = decimal.Decimal(str(entry.get("energy_consumed_kwh", 0)))
            net_energy = energy_generated - energy_consumed
            anomaly = energy_generated < 0 or energy_consumed < 0

            # Store data in DynamoDB
            item = {
                "site_id": site_id,
                "record_timestamp": record_timestamp,  # Updated field name
                "energy_generated_kwh": energy_generated,
                "energy_consumed_kwh": energy_consumed,
                "net_energy_kwh": net_energy,
                "anomaly": anomaly
            }
            print(f" Storing in DynamoDB: {item}")  # Debugging log
            table.put_item(Item=item)

            if anomaly:
                alert_message = (
                    f" **Energy Anomaly Detected!** \n"
                    f" **Site ID:** {site_id}\n"
                    f" **Timestamp:** {record_timestamp}\n"
                    f" **Generated Energy:** {energy_generated} kWh\n"
                    f" **Consumed Energy:** {energy_consumed} kWh\n"
                    f" **Anomaly Detected!**"
                )
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=alert_message,
                    Subject=" Energy Anomaly Alert!"
                )

                

        print(f" Processed {len(energy_data)} records from {object_key}")

    return {"statusCode": 200, "body": "Processing complete"}
