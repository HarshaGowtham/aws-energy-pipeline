import os
import json
import boto3
from decimal import Decimal

# Initialize AWS clients
dynamodb = boto3.resource("dynamodb")
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]

def decimal_to_float(obj):
    """Convert Decimal types to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    """API to query energy data by site_id."""
    
    # Parse query parameters from API Gateway request
    query_params = event.get("queryStringParameters", {})
    if not query_params or "site_id" not in query_params:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required parameter: site_id"})
        }
    
    site_id = query_params["site_id"]
    
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    # Query DynamoDB for records matching site_id
    response = table.query(
        KeyConditionExpression="site_id = :s",
        ExpressionAttributeValues={":s": site_id}
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Items", []), default=decimal_to_float)  # ✅ Fix: Convert Decimal
    }
