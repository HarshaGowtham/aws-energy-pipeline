 
import json
import boto3
import random
import time
import schedule
from datetime import datetime
from faker import Faker

# Initialize Faker
fake = Faker()

# AWS S3 Configuration
BUCKET_NAME = "energy-data-bucket-username"  # Replace with your actual bucket name
s3_client = boto3.client("s3")

def generate_energy_data():
    """Generates fake energy data for multiple sites and uploads to S3."""
    data = []
    for _ in range(5):  # Simulate 5 energy sites
        site_data = {
            "site_id": fake.uuid4(),
            "timestamp": datetime.utcnow().isoformat(),
            "energy_generated_kwh": round(random.uniform(0, 500), 2),
            "energy_consumed_kwh": round(random.uniform(0, 500), 2),
        }
        data.append(site_data)

    # Convert to JSON
    json_data = json.dumps(data, indent=2)

    # File name with timestamp
    filename = f"energy_data_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"

    # Upload to S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=f"raw-data/{filename}",
        Body=json_data,
        ContentType="application/json"
    )

    print(f"Uploaded {filename} to S3 bucket {BUCKET_NAME}")

# Schedule the function to run every 5 minutes
schedule.every(5).minutes.do(generate_energy_data)

if __name__ == "__main__":
    print("Starting data generator... Press Ctrl+C to stop.")
    generate_energy_data()  # Run once immediately
    while True:
        schedule.run_pending()
        time.sleep(1)
